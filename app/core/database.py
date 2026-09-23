# ---------------------------------------------------------
# Load Chroma Vector Database
# ---------------------------------------------------------
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

import os

# Uses Hugging Face API — doesn't load model weights locally!
embedding_function = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=settings.huggingfacehub_api_token
)

print("Loaded HF Token:", settings.huggingfacehub_api_token[:5] if settings.huggingfacehub_api_token else "NONE")

vectordb = Chroma(
    persist_directory=settings.chroma_db_path,
    embedding_function=embedding_function,
    collection_name=settings.collection_name,
)


SQLALCHEMY_DATABASE_URL = "sqlite:///./enterprise_rag.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()