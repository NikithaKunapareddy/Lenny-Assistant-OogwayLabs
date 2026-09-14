import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.models_db import Base

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Psycopg2 does not recognize pgbouncer=true as a libpq connection option
if "pgbouncer=true" in db_url:
    if "?pgbouncer=true&" in db_url:
        db_url = db_url.replace("?pgbouncer=true&", "?")
    elif "&pgbouncer=true" in db_url:
        db_url = db_url.replace("&pgbouncer=true", "")
    elif "?pgbouncer=true" in db_url:
        db_url = db_url.replace("?pgbouncer=true", "")

connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

engine = create_engine(
    db_url,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database schema."""
    try:
        Base.metadata.create_all(bind=engine)
        print(f"[+] Database tables initialized successfully ({db_url.split('://')[0]}).")
    except Exception as e:
        print(f"[!] Warning: Database table auto-initialization skipped or failed: {e}")

# Auto-initialize tables immediately
init_db()

def get_db():
    """FastAPI Dependency for database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
