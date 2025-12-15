"""Utility for splitting long documents into overlapping text chunks.

These chunks are what we actually index into the vector store for retrieval.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:
    """
    Wraps LangChain's RecursiveCharacterTextSplitter with sensible defaults.

    These chunks are what we actually index into the vector store.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        # Configure a character‑based splitter that preserves some overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(self, documents):
        """Split a list of LangChain Document objects into smaller chunks."""
        return self.splitter.split_documents(documents)
