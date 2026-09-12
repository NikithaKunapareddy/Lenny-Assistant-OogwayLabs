import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "The Lenny Growth Assistant" in data["message"]

def test_health_endpoints():
    for endpoint in ["/health", "/api/health"]:
        response = client.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert data["database"] == "connected"
        assert data["knowledge_base"]["loaded"] is True
        assert data["knowledge_base"]["total_chunks"] > 100

def test_models_endpoints():
    # 1. List models
    res = client.get("/api/models")
    assert res.status_code == 200
    data = res.json()
    assert "active_provider" in data
    assert len(data["providers"]) >= 3

    # 2. Switch model
    res_switch = client.post("/api/models/switch", json={"provider": "mock"})
    assert res_switch.status_code == 200
    assert res_switch.json()["active_provider"] == "mock"

def test_sessions_lifecycle():
    # Create session
    create_res = client.post("/api/sessions", json={"title": "Test Strategy Session", "model_provider": "mock"})
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["id"]
    assert session_data["title"] == "Test Strategy Session"

    # List sessions
    list_res = client.get("/api/sessions")
    assert list_res.status_code == 200
    session_ids = [s["id"] for s in list_res.json()]
    assert session_id in session_ids

    # Get session details
    detail_res = client.get(f"/api/sessions/{session_id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["id"] == session_id
    assert len(detail_data["messages"]) == 0

    # Delete session
    del_res = client.delete(f"/api/sessions/{session_id}")
    assert del_res.status_code == 204

    # Verify deleted
    get_after_del = client.get(f"/api/sessions/{session_id}")
    assert get_after_del.status_code == 404
