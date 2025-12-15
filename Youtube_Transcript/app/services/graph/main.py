"""Public entrypoint for executing the YouTube transcript RAG graph."""

from langchain_core.messages import HumanMessage

from app.services.graph.youtube_transcript_graph import graph


async def chat(message: str, thread_id: str) -> str:
    """
    Run a single turn of the chat graph and return the final answer text.

    The thread_id is passed through to LangGraph's configurable state to enable
    per‑thread memory via the MemorySaver checkpointer.
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Kick off the graph with the latest user message
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config,
    )

    # The answer_node appends the final LLM response to the messages list
    return result["messages"][-1].content