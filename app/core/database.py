# ---------------------------------------------------------
# Load Chroma Vector Database
# ---------------------------------------------------------
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

embedding_function = SentenceTransformerEmbeddings(
    model_name=settings.embedding_model
)

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