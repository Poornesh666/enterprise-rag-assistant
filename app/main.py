"""
main.py
--------
FastAPI backend for the Enterprise RAG Assistant.

Features:
- JWT-based authentication
- Role-based document retrieval (RBAC)
- ChromaDB vector search
- Ollama LLM integration
"""
# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.core.logging import logger
from app.core.exceptions import global_exception_handler

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Role-Based AI Assistant powered by FastAPI, ChromaDB, Ollama and JWT.",
    version="2.0.0",
)

logger.info("Enterprise RAG Assistant started successfully.")

app.add_exception_handler(
    Exception,
    global_exception_handler,
)

app.include_router(auth_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # should tighten this later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Health check endpoint
@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy"
    }