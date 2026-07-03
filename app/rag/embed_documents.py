"""
embed_documents.py
------------------
Loads department documents, splits them into chunks,
creates embeddings, and stores them in ChromaDB.
"""

from pathlib import Path
import shutil

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    CSVLoader,
    TextLoader,
    UnstructuredFileLoader,
)
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from app.core.config import settings


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DOCUMENTS_DIR = Path("resources/documents")
CHROMA_DIR = Path(settings.chroma_db_path)

embedding_model = SentenceTransformerEmbeddings(
    model_name=settings.embedding_model
)


# ---------------------------------------------------------
# Build Chroma Vector Database
# ---------------------------------------------------------

def build_vector_database() -> None:
    """
    Load documents, generate embeddings,
    and store them in ChromaDB.
    """

    all_split_docs = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    for department in DOCUMENTS_DIR.iterdir():

        if not department.is_dir():
            continue

        print(f"\nProcessing: {department.name}")

        documents = []

        for file_path in department.iterdir():

            try:

                if file_path.suffix == ".md":

                    try:
                        loader = UnstructuredFileLoader(str(file_path))
                        docs = loader.load()

                    except Exception:
                        loader = TextLoader(str(file_path), encoding="utf-8")
                        docs = loader.load()

                elif file_path.suffix == ".csv":

                    loader = CSVLoader(str(file_path))
                    docs = loader.load()

                else:
                    continue

                documents.extend(docs)

            except Exception as e:
                print(f"Failed to load {file_path.name}: {e}")

        if not documents:
            print(f"No documents found in '{department.name}'")
            continue

        split_docs = splitter.split_documents(documents)

        for doc in split_docs:
            doc.metadata = {
                "role": department.name.lower(),
                "category": (
                    "general"
                    if department.name.lower() == "general"
                    else department.name.lower()
                ),
            }

        all_split_docs.extend(split_docs)

        print(f"Embedded {len(split_docs)} chunks")

    # ---------------------------------------------------------
    # Rebuild Chroma Database
    # ---------------------------------------------------------

    shutil.rmtree(CHROMA_DIR, ignore_errors=True)

    db = Chroma.from_documents(
        documents=all_split_docs,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DIR),
        collection_name=settings.collection_name,
    )

    db.persist()

    print("\nEmbedding completed successfully!")
    print(f"Total Chunks: {len(all_split_docs)}")
    print(f"Chroma Path : {CHROMA_DIR}")

    metadata = db._collection.get()["metadatas"][:5]
    print(f"Sample Metadata: {metadata}")


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    build_vector_database()
