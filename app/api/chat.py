# =========================================================
# Chat Endpoint
# =========================================================

from email import message

from fastapi import APIRouter, Depends, HTTPException
from app.rag.llm import generate_response

from app.core.config import settings
from app.core.security import get_current_user
from app.schemas.chat import ChatRequest
from app.rag.retriever import retrieve_documents
from app.rag.pipeline import build_prompt

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a role-aware response using RAG + Ollama.
    """
    docs = retrieve_documents(
        query=request.message,
        role=current_user["role"],
    )
    
    if not docs:
        raise HTTPException(
            status_code=404,
            detail=f"No documents found for role '{current_user['role']}'.",
        )

    # -----------------------------
    # Build Prompt
    # -----------------------------
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = build_prompt(
     context=context,
     role=current_user["role"],
     question=request.message,
  )

    llm_answer = generate_response(prompt)

    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "query": request.message,
        "response": llm_answer,
    } 