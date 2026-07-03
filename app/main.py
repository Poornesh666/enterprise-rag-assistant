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

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Role-Based AI Assistant powered by FastAPI, ChromaDB, Ollama and JWT.",
    version="2.0.0",
)

app.include_router(auth_router)
app.include_router(chat_router)