"""Graph node that retrieves relevant transcript chunks from Chroma."""

import logging

from app.core.config import settings
from app.core.factory import get_embeddings
from app.infrastructure.chroma.repository import ChromaVectorRepository
from app.services.graph.youtube_transcript_graph_state import RAGState


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Shared vector repository reused across node invocations
vector_repo = ChromaVectorRepository(
    embeddings=get_embeddings(),
    persist_dir=settings.CHROMA_PERSIST_DIR if settings.IS_CHROMA_PERSISTENT else None,
)


async def retrieve_node(state: RAGState) -> dict:
    """
    Retrieve relevant chunks from the vector store for the latest user message.

    Returns:
        dict with:
        - context: joined content of top‑k retrieved chunks
        - all_context: concatenation of all stored documents, used as a
          stronger guardrail in the answer node.
    """
    logger.info("=== RETRIEVE NODE CALLED ===")

    # Use the latest message text as the retrieval query
    query = state["messages"][-1].content

    vector_store = vector_repo.get_vector_store(collection_name="youtube_transcripts")

    # Asynchronous retriever over Chroma via LangChain
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = await retriever.ainvoke(query)
    logger.info(f"Retrieved {len(docs)} documents from vector store")

    # Join retrieved pages into a single context string
    context = "\n---\n".join(d.page_content for d in docs)
    logger.info(f"retrieved data : {context}")

    try:
        # Optionally pull all stored documents for stricter off‑topic detection
        all_docs_result = vector_store.get(include=["documents"])
        all_context = "\n---\n".join(all_docs_result["documents"])

        logger.info(f"Retrieved total {len(all_docs_result['documents'])} documents for all_context")

    except Exception as e:
        logger.warning(f"Could not retrieve all context: {e}")
        all_context = context

    logger.info("Retrieved relevant + full context")
    return {"context": context, "all_context": all_context}