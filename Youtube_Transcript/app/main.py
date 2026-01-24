"""FastAPI entrypoint for the YouTube Transcript RAG backend."""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router


# Main FastAPI application instance
app = FastAPI(
    title="YouTube RAG API",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "paramiwijesinghe05@gmail.com",
    },
)

# Allow cross‑origin requests for the simple HTML/JS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount versioned API routes under /api/v1
app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["Health"], summary="Check API health")
def health_check() -> dict:
    """Simple liveness endpoint used by containers / monitoring."""
    return {"status": "ok"}


# Serve static files (frontend) from the frontend directory
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
