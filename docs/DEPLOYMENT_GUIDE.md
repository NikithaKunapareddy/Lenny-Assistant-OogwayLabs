# Lenny Growth Assistant - Deployment & Setup Guide

This guide covers local development, Docker Compose multi-container deployment, and production scaling.

---

## 1. Local Development Quickstart

### Prerequisites
* Python 3.10+
* Node.js 18+
* Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## 2. Docker Compose Deployment

Run the entire stack with a single command:
```bash
docker compose up --build -d
```

### Services Included:
1. **Backend**: FastAPI API running on port 8000.
2. **Frontend**: Vite/React web app served via Nginx on port 3000.
3. **Ollama**: Local LLM runner (llama3.2:3b) on port 11434.

---

## 3. Environment Variables

Create a `.env` file in the root directory:
```env
APP_ENV=production
LOG_LEVEL=info
OLLAMA_BASE_URL=http://localhost:11434
SUPABASE_URL=
SUPABASE_KEY=
```
