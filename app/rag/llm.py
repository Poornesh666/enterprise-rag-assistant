# ---------------------------------------------------------
# Query Groq LLM
# ---------------------------------------------------------

from groq import Groq
from fastapi import HTTPException

from app.core.config import settings

client = Groq(
    api_key=settings.groq_api_key,
)


def generate_response(prompt: str) -> str:
    # --- ADD DEBUG PRINTS HERE ---
    print(f"DEBUG: Using Model -> '{settings.groq_model}'")
    print(f"DEBUG: Using API Key -> '{settings.groq_api_key[:8]}...'")
    # -----------------------------

    try:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Groq service unavailable: {str(e)}",
        )
        
    