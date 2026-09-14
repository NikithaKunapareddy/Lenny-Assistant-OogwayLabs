import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "The Lenny Growth Assistant"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Database: Supports SQLite for zero-setup local dev and PostgreSQL for production / Docker / Supabase / Railway
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'lenny_assistant.db'))}"
    )

    # LLM Configuration: Default to 'mock' for instant (<2s) responses, toggleable to 'ollama' / 'openai' / 'anthropic'
    DEFAULT_MODEL_PROVIDER: str = os.getenv("DEFAULT_MODEL_PROVIDER", "mock")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "8"))

    # CORS: comma-separated origins for production (e.g. "https://myapp.com,https://www.myapp.com")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # RAG Settings
    RAG_GROUNDING_THRESHOLD: float = float(os.getenv("RAG_GROUNDING_THRESHOLD", "0.05"))
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "4"))

    # Supabase Settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_PUBLISHABLE_KEY: str = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    SUPABASE_SECRET_KEY: str = os.getenv("SUPABASE_SECRET_KEY", "")
    SUPABASE_JWKS_URL: str = os.getenv("SUPABASE_JWKS_URL", "")
    DIRECT_URL: str = os.getenv("DIRECT_URL", "")

    class Config:
        env_file = (".env", "../.env")
        extra = "allow"

settings = Settings()
