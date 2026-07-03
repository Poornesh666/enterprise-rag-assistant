from app.core.database import vectordb
from app.core.config import settings

def retrieve_documents(query: str, role: str):
    """
    Retrieve documents from ChromaDB based on the user's role.
    """

    role = role.lower()
    top_k = settings.top_k

    if role == "c-levelexecutives":
        docs = vectordb.similarity_search(
            query,
            k=top_k,
        )
        if not docs:
            docs = vectordb.similarity_search(
                query,
                k=top_k,
                filter={
                    "role": {
                        "$in": [
                            "engineering",
                            "finance",
                            "hr",
                            "marketing",
                            "general",
                        ]
                    }
                },
            )
    elif role == "employee":
        docs = vectordb.similarity_search(
            query,
            k=top_k,
            filter={"category": "general"},
        )
    else:
        docs = vectordb.similarity_search(
            query,
            k=top_k,
            filter={"role": role},
        )
    return docs