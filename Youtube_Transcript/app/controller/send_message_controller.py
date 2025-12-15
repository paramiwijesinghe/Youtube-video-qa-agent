"""Controller that forwards chat messages into the LangGraph RAG pipeline."""

from fastapi import HTTPException

from app.models.schemas import ChatRequest
from app.services.graph.main import chat


async def send_message_controller(request: ChatRequest) -> dict:
    """
    Execute a single turn of the chat graph.

    The underlying graph handles:
    - retrieving relevant chunks from Chroma
    - calling the LLM with strict system instructions
    - returning the final answer text
    """
    try:
        # Delegate to the async chat graph entrypoint
        answer = await chat(
            request.message,
            request.thread_id,
        )
        return {
            "thread_id": request.thread_id,
            "answer": answer,
        }

    except Exception as e:  # Surface errors as HTTP 500
        raise HTTPException(status_code=500, detail=str(e))
