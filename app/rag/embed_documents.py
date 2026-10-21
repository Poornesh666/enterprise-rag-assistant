
"""
embed_documents.py
------------------
Loads department documents, splits them into chunks,
creates embeddings, and stores them in ChromaDB.
"""

import shutil
import uuid
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    CSVLoader,
    TextLoader,
    UnstructuredFileLoader,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.core.config import settings


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DOCUMENTS_DIR = Path("resources/documents")
CHROMA_DIR = Path(settings.chroma_db_path)

EXPECTED_DEPARTMENTS = {
    "engineering",
    "finance",
    "general",
    "hr",
    "marketing",
}

embedding_model = HuggingFaceEmbeddings(
    model_name=settings.embedding_model
)


# ---------------------------------------------------------
# Build Chroma Vector Database
# ---------------------------------------------------------

def build_vector_database() -> None:
    """
    Load department documents, validate metadata, split them
    into chunks, and safely rebuild the ChromaDB index.
    """

    # Validate the source directory.
    if not DOCUMENTS_DIR.is_dir():
        raise FileNotFoundError(
            f"Documents directory does not exist: {DOCUMENTS_DIR}"
        )

    departments = sorted(
        (
            path for path in DOCUMENTS_DIR.iterdir()
            if path.is_dir()
        ),
        key=lambda path: path.name.lower(),
    )

    if not departments:
        raise ValueError(
            f"No department folders found in {DOCUMENTS_DIR}"
        )

    unknown_departments = {
        department.name.lower()
        for department in departments
    } - EXPECTED_DEPARTMENTS

    if unknown_departments:
        raise ValueError(
            f"Unknown department folders: {sorted(unknown_departments)}"
        )

    # Load and split source documents.
    all_split_docs = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    for department in departments:
        department_name = department.name.lower()

        print(f"\nProcessing: {department_name}")

        documents = []

        for file_path in sorted(department.iterdir()):
            if not file_path.is_file():
                continue

            try:
                suffix = file_path.suffix.lower()

                if suffix == ".md":
                    try:
                        loader = UnstructuredFileLoader(str(file_path))
                        docs = loader.load()
                    except Exception:
                        # Markdown can still be loaded as plain text.
                        loader = TextLoader(
                            str(file_path),
                            encoding="utf-8",
                        )
                        docs = loader.load()

                elif suffix == ".csv":
                    loader = CSVLoader(str(file_path))
                    docs = loader.load()

                else:
                    print(
                        f"Skipping unsupported file: {file_path.name}"
                    )
                    continue

                # Derive access-control metadata from the trusted
                # directory structure, not from document contents.
                for doc in docs:
                    doc.metadata["source"] = file_path.name
                    doc.metadata["role"] = department_name
                    doc.metadata["category"] = (
                        "general"
                        if department_name == "general"
                        else department_name
                    )

                documents.extend(docs)

            except Exception as exc:
                print(f"Failed to load {file_path.name}: {exc}")

        if not documents:
            print(
                f"No usable documents found in '{department_name}'"
            )
            continue

        split_docs = splitter.split_documents(documents)

        if not split_docs:
            print(
                f"No chunks generated for '{department_name}'"
            )
            continue

        all_split_docs.extend(split_docs)
        print(f"Prepared {len(split_docs)} chunks")

    # Never replace the existing index with an empty index.
    if not all_split_docs:
        raise ValueError(
            "No document chunks were generated. "
            "The existing ChromaDB index has not been changed."
        )

    # ---------------------------------------------------------
    # Build and verify a replacement index
    # ---------------------------------------------------------

    CHROMA_DIR.parent.mkdir(parents=True, exist_ok=True)

    temp_dir = CHROMA_DIR.parent / (
        f"{CHROMA_DIR.name}_build_{uuid.uuid4().hex}"
    )
    backup_dir = CHROMA_DIR.parent / f"{CHROMA_DIR.name}_backup"

    try:
        db = Chroma.from_documents(
            documents=all_split_docs,
            embedding=embedding_model,
            persist_directory=str(temp_dir),
            collection_name=settings.collection_name,
        )

        # Confirm that all expected chunks were stored.
        stored_count = db._collection.count()

        if stored_count != len(all_split_docs):
            raise RuntimeError(
                f"Index verification failed: expected "
                f"{len(all_split_docs)} chunks, "
                f"found {stored_count}"
            )

        # Refuse to overwrite a previous backup automatically.
        if backup_dir.exists():
            raise FileExistsError(
                f"Backup directory already exists: {backup_dir}. "
                "Inspect or move it before rebuilding."
            )

        had_existing_index = CHROMA_DIR.exists()

        # Move the current index aside before activating the new one.
        if had_existing_index:
            CHROMA_DIR.rename(backup_dir)

        try:
            temp_dir.rename(CHROMA_DIR)

        except Exception:
            # Attempt to restore the previous index.
            if had_existing_index and backup_dir.exists():
                backup_dir.rename(CHROMA_DIR)
            raise

        # The replacement is active. Remove the old backup only
        # after successful activation; if cleanup fails, retain it.
        if backup_dir.exists():
            try:
                shutil.rmtree(backup_dir)
            except OSError as exc:
                print(
                    f"WARNING: New index is active, but backup "
                    f"cleanup failed: {exc}"
                )
                print(f"Backup retained at: {backup_dir}")

    finally:
        # Clean up an incomplete temporary index after failure.
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

    # Report success only after the replacement is activated.
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
