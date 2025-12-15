"""Controller responsible for building the vector store from a YouTube URL."""

from fastapi import HTTPException

from app.core.config import settings
from app.core.factory import get_embeddings
from app.infrastructure.chroma.repository import ChromaVectorRepository
from app.services.document_splitter_service import DocumentSplitter
from app.services.youtube_loader_service import YoutubeTranscriptLoader


# Long‑lived helpers reused across requests
loader = YoutubeTranscriptLoader()
splitter = DocumentSplitter()

# Repository abstraction around the Chroma vector store
vector_repo = ChromaVectorRepository(
    embeddings=get_embeddings(),
    persist_dir=settings.CHROMA_PERSIST_DIR if settings.IS_CHROMA_PERSISTENT else None,
)


async def initialize_chat_controller(url: str) -> dict:
    """
    Ingest a YouTube transcript and (re)build the vector store.

    This:
    - loads the transcript from YouTube
    - splits it into overlapping chunks
    - saves all chunks into a single "youtube_transcripts" collection,
      clearing any previous content.
    """
    try:
        # 1) Load raw transcript documents for the URL
        documents = loader.load(url)

        # 2) Split into smaller, retriever‑friendly chunks
        chunks = splitter.split(documents)

        # 3) Persist chunks into Chroma (optionally clearing existing data)
        vector_repo.save(
            documents=chunks,
            collection_name="youtube_transcripts",
            clear_existing=True,
        )

        return {
            "status": "ready",
            "message": f"Knowledge base cleared and updated with new video. Total chunks: {len(chunks)}",
        }
    except Exception as e:  # Let FastAPI convert this into a 500 response
        raise HTTPException(status_code=500, detail=str(e))

