"""API route definitions for the YouTube RAG service.

This layer is intentionally thin and delegates real work to controller modules.
"""

from fastapi import APIRouter

from app.controller.initialize_chat_controller import initialize_chat_controller
from app.controller.send_message_controller import send_message_controller
from app.models.schemas import ChatRequest, InitChatRequest


# All routes under /api/v1 are registered on this router in app/main.py
router = APIRouter()


@router.post("/init", status_code=201)
async def initialize_chat(request: InitChatRequest) -> dict:
    """
    Initialize / reset the knowledge base for a given YouTube URL.

    - Downloads the transcript for the given URL
    - Splits it into text chunks suited for retrieval
    - Indexes chunks into the Chroma vector store
    """
    return await initialize_chat_controller(str(request.url))


@router.post("/message")
async def send_message(request: ChatRequest) -> dict:
    """Send a chat message to the RAG graph and return the model's answer."""
    return await send_message_controller(request)
