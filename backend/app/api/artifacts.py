from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.models_db import Artifact

router = APIRouter(prefix="/artifacts", tags=["Artifacts"])

@router.get("/{artifact_id}")
def get_artifact(artifact_id: str, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail=f"Artifact '{artifact_id}' not found")
    return {
        "id": artifact.id,
        "session_id": artifact.session_id,
        "message_id": artifact.message_id,
        "title": artifact.title,
        "artifact_type": artifact.artifact_type,
        "content": artifact.content,
        "version": artifact.version,
        "created_at": artifact.created_at
    }

@router.get("/session/{session_id}")
def list_session_artifacts(session_id: str, db: Session = Depends(get_db)):
    artifacts = db.query(Artifact).filter(Artifact.session_id == session_id).order_by(Artifact.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "session_id": a.session_id,
            "message_id": a.message_id,
            "title": a.title,
            "artifact_type": a.artifact_type,
            "content": a.content,
            "created_at": a.created_at
        }
        for a in artifacts
    ]
