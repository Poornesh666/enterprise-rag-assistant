# ---------------------------------------------------------
# Load Chroma Vector Database
# ---------------------------------------------------------
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from app.core.config import settings

embedding_function = SentenceTransformerEmbeddings(
    model_name=settings.embedding_model
)

vectordb = Chroma(
    persist_directory=settings.chroma_db_path,
    embedding_function=embedding_function,
    collection_name=settings.collection_name,
)