"""Shared state definition for the YouTube transcript RAG LangGraph.

Each node in the graph reads from and writes to this TypedDict-based state.
"""

from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class RAGState(TypedDict):
    """
    State that flows between graph nodes.

    - messages: running chat history (user + assistant)
    - context: retrieved chunk(s) for the current question
    - all_context: concatenation of all stored chunks (used as extra guardrail)
    """

    messages: Annotated[List[BaseMessage], add_messages]
    context: str
    all_context: str
