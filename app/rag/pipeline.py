"""
pipeline.py
-----------
Builds the prompt passed to the LLM.
"""


def build_prompt(
    context: str,
    role: str,
    question: str,
) -> str:
    """
    Build a prompt using the retrieved context and user's role.
    """

    prompt = f"""
You are an AI assistant at FinSolve Technologies.

The user's role is: {role}.

Answer using ONLY the provided context.
If the answer is not available in the context, politely say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt