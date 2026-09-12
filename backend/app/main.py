import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import init_db
from app.api.router import api_router
from app.api.health import router as root_health_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-grade AI assistant powered by Lenny's Podcast transcripts.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Structured request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start_time) * 1000)
    print(f"[{request.method}] {request.url.path} -> Status {response.status_code} ({duration_ms}ms)")
    return response

# Structured Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[!] Unhandled error on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "path": request.url.path
        }
    )

@app.on_event("startup")
def on_startup():
    print("==================================================")
    print(f" Starting {settings.APP_NAME} ({settings.APP_ENV})")
    print("==================================================")
    init_db()

# Include routers
app.include_router(root_health_router)
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "health": "/health"
    }
