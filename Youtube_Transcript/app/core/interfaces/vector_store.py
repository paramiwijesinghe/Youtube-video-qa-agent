"""Abstract interface for a vector store implementation."""

from abc import ABC, abstractmethod
from typing import Any, List


class VectorStore(ABC):
    """Defines the operations required by the rest of the app for a vector store."""

    @abstractmethod
    def add_documents(self, documents: List[Any], collection_name: str) -> None:
        """Append new documents to an existing collection."""

    @abstractmethod
    def get_vector_store(self, collection_name: str) -> Any:
        """Return the underlying vector store client for advanced operations."""

    @abstractmethod
    def clear_collection(self, collection_name: str) -> None:
        """Remove all documents from a specific collection."""

    @abstractmethod
    def save(
        self,
        documents: List[Any],
        collection_name: str,
        clear_existing: bool = True,
    ) -> None:
        """
        Save documents into a collection.

        If clear_existing=True, any existing collection with the same name
        should be deleted before saving.
        """
