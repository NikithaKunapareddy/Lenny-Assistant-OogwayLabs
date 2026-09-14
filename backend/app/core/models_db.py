import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), default="New Strategy Chat", nullable=False)
    model_provider = Column(String(64), default="mock", nullable=False)
    model_name = Column(String(128), default="llama3:latest", nullable=False)
    session_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    artifacts = relationship("Artifact", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(64), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(32), nullable=False) # 'user' | 'assistant' | 'system'
    content = Column(Text, nullable=False)
    sources = Column(JSON, default=list)
    token_count = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    skill_used = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    session = relationship("Session", back_populates="messages")
    artifacts = relationship("Artifact", back_populates="message", cascade="all, delete-orphan")

class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(64), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    message_id = Column(String(64), ForeignKey("messages.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    artifact_type = Column(String(32), default="html") # 'html' | 'markdown' | 'svg'
    content = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    session = relationship("Session", back_populates="artifacts")
    message = relationship("Message", back_populates="artifacts")
