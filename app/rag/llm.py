# app/rag/llm.py
# -----------------------------
# Query Ollama
# -----------------------------

import requests
from fastapi import HTTPException

from app.core.config import settings


def generate_response(prompt: str) -> str:
    """
    Send the prompt to Ollama and return the generated response.
    """

    response = requests.post(
        settings.ollama_url,
        json={
            "model": settings.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
            },
        },
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="Unable to reach the Ollama service.",
        )

    return response.json()["response"]