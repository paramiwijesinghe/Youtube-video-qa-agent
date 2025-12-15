"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration object. Values are populated from .env / env vars."""

    # LLM / embeddings credentials
    OPENAI_API_KEY: str
    HF_TOKEN: str

    # Chroma persistence configuration
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    IS_CHROMA_PERSISTENT: bool = False

    # LLM configuration
    MODEL_NAME: str = "gpt-4o-mini"
    LLM_PROVIDER: str = "openai"  # openai, google, anthropic

    # Embedding model configuration
    EMBEDDING_MODEL: str = "BAAI/bge-m3"
    EMBEDDING_PROVIDER: str = "huggingface"  # openai, google, huggingface

    class Config:
        env_file = ".env"


# Singleton settings instance imported across the app
settings = Settings()