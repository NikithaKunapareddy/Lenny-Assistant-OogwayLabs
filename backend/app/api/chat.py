import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.models_db import Session as DbSession, Message, Artifact
from app.agent.orchestrator import agent_orchestrator
from app.llm.factory import llm_manager

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(..., min_length=1, description="User question or prompt")
    model_provider: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    response: str
    sources: List[Dict[str, Any]]
    artifact: Optional[Dict[str, Any]] = None
    routed_intent: str
    skill_used: str
    latency_ms: int
    is_grounded: bool
    model_provider: str

@router.post("", response_model=ChatResponse)
def send_chat_message(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. Resolve or create session
    session = None
    if req.session_id:
        session = db.query(DbSession).filter(DbSession.id == req.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail=f"Session '{req.session_id}' not found")
    else:
        # Create new session automatically
        provider = req.model_provider or llm_manager.active_provider
        session = DbSession(
            title="New Strategy Chat",
            model_provider=provider,
            model_name="llama3:latest" if provider == "ollama" else provider
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Persist User Message
    user_msg = Message(
        session_id=session.id,
        role="user",
        content=req.message
    )
    db.add(user_msg)
    db.commit()

    # 3. Assemble previous conversation history
    past_messages = sorted(session.messages, key=lambda m: m.created_at)
    history = [
        {"role": m.role, "content": m.content}
        for m in past_messages[:-1] # exclude the user message just added
    ]

    # 4. Execute Agent Orchestrator
    try:
        agent_result = agent_orchestrator.execute(
            query=req.message,
            conversation_history=history,
            model_provider_override=req.model_provider or session.model_provider
        )
    except Exception as e:
        print(f"[!] Error in agent execution: {e}")
        # Graceful degradation
        agent_result = {
            "content": f"An error occurred while communicating with the model provider: {str(e)}. Please check your model configuration or switch providers.",
            "sources": [],
            "artifact": None,
            "routed_intent": "qna",
            "skill": "error",
            "latency_ms": 0,
            "is_grounded": False,
            "model_provider": req.model_provider or session.model_provider
        }

    # 5. Persist Assistant Message
    assistant_msg = Message(
        session_id=session.id,
        role="assistant",
        content=agent_result["content"],
        sources=agent_result.get("sources", []),
        skill_used=agent_result.get("skill", "qna"),
        latency_ms=agent_result.get("latency_ms", 0)
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    # 6. If an artifact was generated, persist to database
    saved_artifact = None
    if agent_result.get("artifact"):
        art_data = agent_result["artifact"]
        db_artifact = Artifact(
            session_id=session.id,
            message_id=assistant_msg.id,
            title=art_data.get("title", "Growth Framework"),
            artifact_type=art_data.get("type", "html"),
            content=art_data.get("content", "")
        )
        db.add(db_artifact)
        db.commit()
        db.refresh(db_artifact)
        saved_artifact = {
            "id": db_artifact.id,
            "title": db_artifact.title,
            "type": db_artifact.artifact_type,
            "content": db_artifact.content
        }

    # 7. Update Session Title if this is the first interaction
    if len(past_messages) <= 1:
        truncated_title = req.message[:40] + ("..." if len(req.message) > 40 else "")
        session.title = truncated_title
    session.updated_at = datetime.now(timezone.utc)
    db.add(session)
    db.commit()

    return ChatResponse(
        session_id=session.id,
        message_id=assistant_msg.id,
        response=agent_result["content"],
        sources=agent_result.get("sources", []),
        artifact=saved_artifact,
        routed_intent=agent_result.get("routed_intent", "qna"),
        skill_used=agent_result.get("skill", "qna"),
        latency_ms=agent_result.get("latency_ms", 0),
        is_grounded=agent_result.get("is_grounded", True),
        model_provider=agent_result.get("model_provider", session.model_provider)
    )

@router.post("/stream")
async def stream_chat_message(req: ChatRequest, db: Session = Depends(get_db)):
    """SSE streaming endpoint for real-time token delivery."""
    chat_res = send_chat_message(req, db)

    async def event_generator():
        words = chat_res.response.split(" ")
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            data = {"type": "token", "token": chunk}
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(0.012)

        final_payload = {
            "type": "final",
            "session_id": chat_res.session_id,
            "message_id": chat_res.message_id,
            "sources": chat_res.sources,
            "artifact": chat_res.artifact,
            "latency_ms": chat_res.latency_ms,
            "skill_used": chat_res.skill_used,
            "is_grounded": chat_res.is_grounded,
            "model_provider": chat_res.model_provider
        }
        yield f"data: {json.dumps(final_payload)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
