"""LangGraph definition for the YouTube transcript RAG pipeline.

The graph is intentionally simple:
- retrieve_node: pulls relevant chunks from the vector store
- answer_node: calls the LLM with strict context-only instructions.
"""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.services.graph.nodes.answer_node import answer_node
from app.services.graph.nodes.retrieve_node import retrieve_node
from app.services.graph.youtube_transcript_graph_state import RAGState


# Build a simple 2‑node graph: retrieve -> answer
builder = StateGraph(RAGState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("answer", answer_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "answer")
builder.add_edge("answer", END)

# In‑memory checkpointer that keeps per‑thread message history
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)