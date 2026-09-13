"""
Shared pytest fixtures for test isolation.
Uses an in-memory SQLite database per test session so tests never
share or accumulate state across runs.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend root is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ─── Override DATABASE_URL before any app module loads ────────────────────────
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.core.models_db import Base
from app.core.database import get_db
from app.main import app

# Create a shared in-memory engine for the test session
_test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)
_TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


def override_get_db():
    db = _TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables once per test session in the in-memory DB."""
    Base.metadata.create_all(bind=_test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=_test_engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def client():
    """Shared TestClient for the entire test session."""
    with TestClient(app) as c:
        yield c
