import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_chat_grounded_qna():
    # 1. Ask a question
    payload = {
        "message": "How do I improve user retention in B2B SaaS?",
        "model_provider": "mock"
    }
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["session_id"] is not None
    assert data["routed_intent"] == "qna"
    assert data["is_grounded"] is True
    assert len(data["sources"]) > 0
    # Check that sources cite real podcast episodes
    first_source = data["sources"][0]
    assert "guest" in first_source
    assert "title" in first_source
    assert "timestamp" in first_source

def test_chat_ship30_essay_generation():
    # 1. Request Ship 30 essay
    payload = {
        "message": "Can you turn this into a Ship 30 for 30 essay about retention?",
        "model_provider": "mock"
    }
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["routed_intent"] == "ship30"
    assert data["skill_used"] == "ship30"
    content = data["response"]
    word_count = len(content.split())
    # Mock engine generates comprehensive long-form content; assert substantial length
    # Real Ollama/Claude output should be ~1,250 words (max_tokens=1800)
    assert word_count > 900, f"Ship30 essay too short: {word_count} words (expected > 900)"
    assert "##" in content  # Markdown headings
    assert "Step" in content or "Protocol" in content or "Framework" in content

def test_chat_artifact_generation_and_sanitization():
    # 1. Request Framework Artifact
    payload = {
        "message": "Create a retention audit framework with an HTML checklist",
        "model_provider": "mock"
    }
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["routed_intent"] == "artifact"
    assert data["artifact"] is not None
    artifact = data["artifact"]
    assert "title" in artifact
    assert artifact["type"] == "html"
    assert "<style>" in artifact["content"]
    # Verify security: no raw malicious script tags
    assert "<script>" not in artifact["content"].lower()

def test_session_context_isolation():
    # 1. Create Session A and ask about PMF
    res_a = client.post("/api/chat", json={"message": "What is the 40% PMF rule by Sean Ellis?", "model_provider": "mock"})
    assert res_a.status_code == 200
    session_a_id = res_a.json()["session_id"]

    # 2. Create Session B and ask about Elena Verna
    res_b = client.post("/api/chat", json={"message": "What does Elena Verna say about B2B growth?", "model_provider": "mock"})
    assert res_b.status_code == 200
    session_b_id = res_b.json()["session_id"]

    assert session_a_id != session_b_id

    # 3. Verify history of Session A only contains Sean Ellis
    history_a = client.get(f"/api/sessions/{session_a_id}").json()
    assert len(history_a["messages"]) == 2 # 1 user, 1 assistant
    assert any("Sean Ellis" in m["content"] for m in history_a["messages"])
    assert not any("Elena Verna" in m["content"] for m in history_a["messages"] if m["role"] == "user")

    # 4. Verify history of Session B only contains Elena Verna
    history_b = client.get(f"/api/sessions/{session_b_id}").json()
    assert len(history_b["messages"]) == 2
    assert any("Elena Verna" in m["content"] for m in history_b["messages"])
