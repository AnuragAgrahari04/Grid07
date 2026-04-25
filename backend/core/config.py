"""Single source of truth for all configuration."""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str | None = None
    LLM_PROVIDER: Literal["auto", "groq", "fallback"] = "auto"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "llama-3.1-8b-instant"
    CHROMA_COLLECTION_NAME: str = "grid07_personas"
    SIMILARITY_THRESHOLD: float = 0.45
    BACKEND_PORT: int = 8000
    BACKEND_HOST: str = "0.0.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
