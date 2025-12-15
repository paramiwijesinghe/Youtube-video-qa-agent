"""Concrete VectorStore implementation backed by Chroma + LangChain."""

from typing import Any, List, Optional

from langchain_chroma import Chroma

from app.core.interfaces.vector_store import VectorStore
from app.infrastructure.chroma.client import ChromaClientFactory


class ChromaVectorRepository(VectorStore):
    """
    Adapter that exposes a minimal vector‑store interface over a Chroma backend.

    This is used both for:
    - initial ingestion (saving all chunks)
    - retrieval via LangChain's Chroma wrapper.
    """

    def __init__(self, embeddings: Any, persist_dir: Optional[str] = None):
        self.embeddings = embeddings
        self.persist_dir = persist_dir
        # Underlying low-level Chroma client (persistent or in-memory)
        self.client = ChromaClientFactory.create_client(persist_dir)
        self._vector_store = None

    def clear_collection(self, collection_name: str) -> None:
        """Delete a collection if it exists, logging failures instead of raising."""
        try:
            self.client.delete_collection(name=collection_name)
            print(f"Collection '{collection_name}' deleted successfully")
        except Exception as e:
            print(f"Collection '{collection_name}' does not exist or error deleting: {e}")

    def save(
        self,
        documents: List[Any],
        collection_name: str,
        clear_existing: bool = True,
    ) -> None:
        """
        Create (or recreate) a collection from a list of documents.

        If clear_existing=True, any existing collection with the same name is
        dropped before building a new one.
        """
        if clear_existing:
            self.clear_collection(collection_name)

        kwargs = {
            "documents": documents,
            "embedding": self.embeddings,
            "collection_name": collection_name,
            "client": self.client,
        }

        # When a persistent directory is configured, also persist via LangChain
        if self.persist_dir:
            kwargs["persist_directory"] = self.persist_dir

        self._vector_store = Chroma.from_documents(**kwargs)

    def get_vector_store(self, collection_name: str) -> Chroma:
        """Return a LangChain Chroma instance for the given collection."""
        return Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents: List[Any], collection_name: str) -> None:
        """Append additional documents to an existing collection."""
        vector_store = self.get_vector_store(collection_name)
        vector_store.add_documents(documents)
