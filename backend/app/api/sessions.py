from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.models_db import Session as DbSession, Message, Artifact
from app.llm.factory import llm_manager

router = APIRouter(prefix="/sessions", tags=["Sessions"])

class CreateSessionRequest(BaseModel):
    title: Optional[str] = None
    model_provider: Optional[str] = None

class SessionSummary(BaseModel):
    id: str
    title: str
    model_provider: str
    model_name: str
    created_at: datetime
    updated_at: datetime
    message_count: int

@router.post("", status_code=status.HTTP_201_CREATED)
def create_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    provider = req.model_provider or llm_manager.active_provider
    new_session = DbSession(
        title=req.title or "New Strategy Chat",
        model_provider=provider,
        model_name="llama3:latest" if provider == "ollama" else provider
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {
        "id": new_session.id,
        "title": new_session.title,
        "model_provider": new_session.model_provider,
        "model_name": new_session.model_name,
        "created_at": new_session.created_at,
        "updated_at": new_session.updated_at
    }

@router.get("", response_model=List[SessionSummary])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(DbSession).order_by(DbSession.updated_at.desc()).all()

    summaries = []
    for s in sessions:
        msg_count = len(s.messages)
        summaries.append(SessionSummary(
            id=s.id,
            title=s.title,
            model_provider=s.model_provider,
            model_name=s.model_name,
            created_at=s.created_at,
            updated_at=s.updated_at,
            message_count=msg_count
        ))
    return summaries

@router.get("/{session_id}")
def get_session_detail(session_id: str, db: Session = Depends(get_db)):
    session = db.query(DbSession).filter(DbSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    messages = sorted(session.messages, key=lambda m: m.created_at)
    artifacts = sorted(session.artifacts, key=lambda a: a.created_at)

    return {
        "id": session.id,
        "title": session.title,
        "model_provider": session.model_provider,
        "model_name": session.model_name,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "sources": m.sources,
                "skill_used": m.skill_used,
                "latency_ms": m.latency_ms,
                "created_at": m.created_at
            }
            for m in messages
        ],
        "artifacts": [
            {
                "id": a.id,
                "message_id": a.message_id,
                "title": a.title,
                "artifact_type": a.artifact_type,
                "content": a.content,
                "created_at": a.created_at
            }
            for a in artifacts
        ]
    }

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(DbSession).filter(DbSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    db.delete(session)
    db.commit()
    return None
