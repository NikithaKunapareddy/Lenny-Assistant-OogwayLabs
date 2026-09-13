import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import init_db
from app.api.router import api_router
from app.api.health import router as root_health_router

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
    datefmt="%Y-%m-%dT%H:%M:%SZ"
)
logger = logging.getLogger("lenny_assistant")

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-grade AI assistant powered by Lenny's Podcast transcripts.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration — locked down in production, open in local dev
_allowed_origins = (
    ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]
    if settings.APP_ENV == "development"
    else [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins if _allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Structured request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start_time) * 1000)
    logger.info(
        f"method={request.method} path={request.url.path} "
        f"status={response.status_code} duration_ms={duration_ms}"
    )
    return response

# Structured Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"unhandled_error method={request.method} path={request.url.path} "
        f"error_type={exc.__class__.__name__} message={str(exc)}"
    )
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "path": request.url.path
        }
    )

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("=================================================")
    logger.info(f" Starting {settings.APP_NAME} ({settings.APP_ENV})")
    logger.info("=================================================")
    init_db()
    yield
    logger.info(f" Shutting down {settings.APP_NAME}")

app.router.lifespan_context = lifespan

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
