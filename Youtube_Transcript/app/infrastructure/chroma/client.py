"""Factory for creating Chroma clients with or without persistence."""

import os
from typing import Optional

import chromadb


class ChromaClientFactory:
    """Small helper to hide chromadb client creation details."""

    @staticmethod
    def create_client(persist_dir: Optional[str] = None) -> chromadb.ClientAPI:
        """
        Create a Chroma client.

        - If persist_dir is provided, a PersistentClient is used and the
          directory will be created if it does not exist.
        - Otherwise, an in‑memory client is created.
        """
        if persist_dir:
            os.makedirs(persist_dir, exist_ok=True)
            return chromadb.PersistentClient(path=persist_dir)
        else:
            return chromadb.Client()
