"""Graph node that generates an answer strictly from retrieved video context."""

import logging
from langchain_core.prompts import ChatPromptTemplate

from app.core.factory import get_llm
from app.services.graph.youtube_transcript_graph_state import RAGState

# Reuse a single logger and LLM client across invocations
logger = logging.getLogger(__name__)
llm = get_llm()

async def answer_node(state: RAGState) -> dict:
    """
    Take the retrieved context + full context and produce a guarded LLM answer.

    The prompt:
    - strictly instructs the model to only use transcript content
    - asks it to refuse questions that are unrelated to the video
    - appends the new assistant message back into the graph state.
    """

    # System prompt that enforces \"only answer from video context\" behavior
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Answer ONLY using the information below.\n\n"
            "FULL CONTEXT:\n{all_context}\n\n"
            "RETRIEVED CONTEXT:\n{context}\n"
            "If query is not related to the context, please respond I don't know."
        ),
        ("placeholder", "{messages}")
    ])

    # Simple LCEL chain: prompt -> LLM
    chain = prompt | llm

    # Invoke the chain with the current graph state
    response = await chain.ainvoke({
        "context": state["context"],
        "all_context": state["all_context"],
        "messages": state["messages"]
    })

    return {"messages": [response]}
