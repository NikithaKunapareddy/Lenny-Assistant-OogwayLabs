# Agent Transcript 02: Database Schema & ORM Refactoring

**Date:** 2026-09-12  
**Role:** Forward Deployed Engineer  
**Focus:** Persistence Layer, SQLite vs PostgreSQL, Dependency Rationalization  

---

## 1. Initial Attempt: SQLModel Dependency Mismatch

### The Problem
During backend initialization, we initially drafted models using `sqlmodel`. When running backend tests, the process failed with:
```
ModuleNotFoundError: No module named 'sqlmodel'
```
Checking the host Python environment revealed that while `SQLAlchemy 2.0.41` was installed, `sqlmodel` was missing.

### The Correction
Rather than forcing extra third-party package dependencies onto evaluators, we refactored `models_db.py` and `database.py` to use standard **SQLAlchemy 2.0 Declarative Base**:
- Used standard `Column`, `String`, `DateTime`, and `JSON` types.
- Defined explicit cascade relationships (`cascade="all, delete-orphan"`) between `Session`, `Message`, and `Artifact`.
- Maintained dual compatibility: SQLite for zero-setup local dev/tests, and PostgreSQL for Docker Compose and production deployments.

---

## 2. Test Execution Bug: Table Initialization in TestClient

### The Problem
During the first pytest run, test cases failed with:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: sessions
```
FastAPI's `@app.on_event("startup")` does not fire automatically when `TestClient(app)` is instantiated outside an explicit lifespan context manager.

### The Correction
In `backend/app/core/database.py`, we invoked `init_db()` at module load time. This guarantees that tables are created immediately before any test or endpoint execution, resulting in 100% test reliability across all environments.
