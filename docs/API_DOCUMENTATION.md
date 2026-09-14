# Lenny Growth Assistant - API Documentation

The Lenny Growth Assistant backend is built on **FastAPI**, exposing high-performance REST and streaming endpoints.

## Base URL
`http://localhost:8000`

---

## Endpoints

### 1. Chat Completion & Agent Dispatch
* **Method:** `POST`
* **Route:** `/api/chat`
* **Content-Type:** `application/json`

#### Request Body:
```json
{
  "message": "Create a product strategy framework",
  "session_id": "optional-uuid-v4",
  "temperature": 0.2
}
```

#### Response:
```json
{
  "session_id": "018f4320-b428-76d1-8176-b632943e88aa",
  "response": "Here is the comprehensive Product Strategy Stack framework...",
  "skill_used": "artifact_skill",
  "artifact": {
    "type": "html",
    "title": "Product Strategy Stack",
    "content": "<!DOCTYPE html>..."
  },
  "sources": [
    {
      "guest": "Ravi Mehta",
      "title": "How to build your product strategy stack",
      "timestamp": "00:18:43",
      "youtube_url": "https://www.youtube.com/watch?v=tncs0m5pmQg&t=1123s",
      "content": "..."
    }
  ]
}
```

---

### 2. Session Management

#### Fetch Conversation History
* **Method:** `GET`
* **Route:** `/api/sessions/{session_id}`
* **Returns:** Full list of exchanged messages, artifacts, and cited sources.

#### Clear / Delete Session
* **Method:** `DELETE`
* **Route:** `/api/sessions/{session_id}`
* **Returns:** `{ "status": "session deleted" }`

---

### 3. Artifact Viewer & Sandboxing

#### Render Sandboxed Artifact
* **Method:** `GET`
* **Route:** `/api/artifacts/{artifact_id}/view`
* **Headers:** `Content-Security-Policy: default-src 'self' 'unsafe-inline'`

---

### 4. Health & System Status
* **Method:** `GET`
* **Route:** `/health`
* **Response:**
```json
{
  "status": "healthy",
  "retriever_loaded": true,
  "total_chunks": 707,
  "embedding_model": "TF-IDF + Cosine Re-ranking",
  "llm_provider": "ollama / mock_fallback"
}
```
