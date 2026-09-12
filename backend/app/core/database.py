import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.models_db import Base

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

engine = create_engine(
    db_url,
    echo=False,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database schema."""
    Base.metadata.create_all(bind=engine)
    print(f"[+] Database tables initialized successfully ({db_url.split('://')[0]}).")

# Auto-initialize tables immediately
init_db()

def get_db():
    """FastAPI Dependency for database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
