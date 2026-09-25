"""
main.py
--------
FastAPI backend for the Enterprise RAG Assistant.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.core.database import init_db
from app.core.logging import logger
from app.core.exceptions import global_exception_handler

from app.models.users import User

from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------------------------
# Initialize Database
# ---------------------------------------------------------
init_db()


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------
app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Role-Based AI Assistant powered by FastAPI, ChromaDB, Groq and JWT.",
    version="2.0.0",
)


logger.info("Enterprise RAG Assistant started successfully.")


# ---------------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------------
app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------
app.include_router(auth_router)
app.include_router(chat_router)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy"
    }