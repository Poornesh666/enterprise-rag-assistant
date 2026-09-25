# ---------------------------------------------------------
# Load Chroma Vector Database
# ---------------------------------------------------------
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# ---------------------------------------------------------
# Embedding Configuration
# Uses Hugging Face API — doesn't load model weights locally
# ---------------------------------------------------------
embedding_function = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=settings.huggingfacehub_api_token,
)

vectordb = Chroma(
    persist_directory=settings.chroma_db_path,
    embedding_function=embedding_function,
    collection_name=settings.collection_name,
)


# ---------------------------------------------------------
# SQLite Database Configuration
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Initialize Database
# Create tables if they do not already exist
# ---------------------------------------------------------
def init_db():
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# Database Dependency
# Provide a database session to API endpoints
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()