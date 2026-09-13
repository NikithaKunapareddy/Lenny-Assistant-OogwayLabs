from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.rag.retriever import retriever
from app.llm.factory import llm_manager
from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1")).first()
    except Exception as e:
        db_status = f"error: {str(e)}"

    rag_status = {
        "loaded": retriever.is_loaded,
        "total_chunks": len(retriever.chunks),
        "total_indexed": len(retriever.chunk_ids)
    }

    ollama_client = llm_manager._providers["ollama"]
    ollama_online = ollama_client.is_available()

    return {
        "status": "healthy" if db_status == "connected" and retriever.is_loaded else "degraded",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": db_status,
        "knowledge_base": rag_status,
        "llm": {
            "active_provider": llm_manager.active_provider,
            "ollama_online": ollama_online,
            "configured_model": settings.OLLAMA_MODEL
        }
    }
