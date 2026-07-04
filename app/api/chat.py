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
from app.core.logging import logger
from app.schemas.responses import ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a role-aware response using RAG + Ollama.
    """
    logger.info(f"Chat request from user '{current_user['username']}' with role '{current_user['role']}': {request.message}")
    
    docs = retrieve_documents(
        query=request.message,
        role=current_user["role"],
    )
    
    logger.info(f"Retrieved {len(docs)} document(s).")
    
    if not docs:
        logger.warning(f"No documents found for role '{current_user['role']}'.")
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

    logger.info("Response generated successfully.")

    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "query": request.message,
        "response": llm_answer,
    } 