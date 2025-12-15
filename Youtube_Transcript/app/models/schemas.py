"""Pydantic request / response models used by the FastAPI layer."""

from pydantic import BaseModel, HttpUrl


class InitChatRequest(BaseModel):
    """Request body for initializing the knowledge base with a video URL."""

    url: HttpUrl
    # Optional logical thread identifier (useful if you later separate users)
    thread_id: str = "default_user"


class ChatRequest(BaseModel):
    """Single‑turn chat request body."""

    message: str
    thread_id: str = "default_user"


class ChatResponse(BaseModel):
    """Example of a typed response schema (not currently used directly)."""

    response: str