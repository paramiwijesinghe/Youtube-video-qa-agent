# YouTube RAG Chat

A RAG (Retrieval-Augmented Generation) application that allows you to chat with YouTube video transcripts.

## Prerequisites

- Python 3.10+
- API Keys:
    - OpenAI API Key (if using OpenAI)
    - HuggingFace Token (for embeddings)
    - Google API Key (if using Google Gemini)
    - Anthropic API Key (if using Claude)

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory and add your keys:
    ```env
    OPENAI_API_KEY=your_openai_key
    HF_TOKEN=your_huggingface_token
    # Optional:
    # GOOGLE_API_KEY=your_google_key
    # ANTHROPIC_API_KEY=your_anthropic_key
    ```

3.  **Configuration**:
    You can configure the models and providers in `app/core/config.py` or via environment variables:
    - `LLM_PROVIDER`: `openai`, `google`, or `anthropic`
    - `EMBEDDING_PROVIDER`: `openai`, `google`, or `huggingface`
    - `IS_CHROMA_PERSISTENT`: `True` or `False`

## Running with Docker (Recommended)

1.  **Build and Start**:
    ```bash
    docker-compose up --build
    ```

2.  **Access**:
    - Frontend: `http://localhost:3000`
    - Backend API: `http://localhost:8001`

## Running Locally (Manual)

1.  **Start the Backend**:
    ```bash
    uvicorn app.main:app --reload --port 8001
    ```
    *Note: We use port 8001 to match the Docker configuration.*

2.  **Start the Frontend**:
    ```bash
    python3 -m http.server 3000
    ```
    Then open `http://localhost:3000`.

## Usage

1.  Enter a YouTube URL in the input field.
2.  Click "Initialize Knowledge Base".
3.  Once initialized, type your question and click "Send".
