"""Factories for creating LLM and embedding clients based on configuration."""

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import settings


def get_embeddings():
    """Return a LangChain embeddings client for the configured provider."""
    if settings.EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )
    elif settings.EMBEDDING_PROVIDER == "google":
        return GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
        )
    elif settings.EMBEDDING_PROVIDER == "huggingface":
        # Hosted HuggingFace Inference API
        return HuggingFaceEndpointEmbeddings(
            model=settings.EMBEDDING_MODEL,
            task="feature-extraction",
            huggingfacehub_api_token=settings.HF_TOKEN,
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}")


def get_llm():
    """Return a chat LLM client for the configured provider."""
    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0,
            streaming=True,
            api_key=settings.OPENAI_API_KEY,
        )
    elif settings.LLM_PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            temperature=0,
            google_api_key=settings.GOOGLE_API_KEY,
        )
    elif settings.LLM_PROVIDER == "anthropic":
        return ChatAnthropic(
            model=settings.MODEL_NAME,
            temperature=0,
            api_key=settings.ANTHROPIC_API_KEY,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")