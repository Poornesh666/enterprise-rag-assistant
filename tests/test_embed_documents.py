
from pathlib import Path
from unittest.mock import Mock

import pytest

import app.rag.embed_documents as ingestion


def test_missing_documents_directory_fails_before_index_changes(
    monkeypatch,
    tmp_path,
):
    documents_dir = tmp_path / "missing_documents"
    chroma_dir = tmp_path / "chroma_db"

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    with pytest.raises(FileNotFoundError):
        ingestion.build_vector_database()

    assert not chroma_dir.exists()


def test_empty_documents_directory_fails_before_index_changes(
    monkeypatch,
    tmp_path,
):
    documents_dir = tmp_path / "documents"
    documents_dir.mkdir()

    chroma_dir = tmp_path / "chroma_db"

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    with pytest.raises(ValueError, match="No department folders"):
        ingestion.build_vector_database()

    assert not chroma_dir.exists()


def test_unknown_department_fails_before_index_changes(
    monkeypatch,
    tmp_path,
):
    documents_dir = tmp_path / "documents"
    (documents_dir / "unknown_department").mkdir(parents=True)

    chroma_dir = tmp_path / "chroma_db"

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    with pytest.raises(ValueError, match="Unknown department"):
        ingestion.build_vector_database()

    assert not chroma_dir.exists()


def test_empty_chunks_do_not_modify_existing_index(
    monkeypatch,
    tmp_path,
):
    documents_dir = tmp_path / "documents"
    (documents_dir / "engineering").mkdir(parents=True)

    chroma_dir = tmp_path / "chroma_db"
    chroma_dir.mkdir()
    marker = chroma_dir / "existing_index.txt"
    marker.write_text("existing index", encoding="utf-8")

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    class EmptySplitter:
        def __init__(self, **kwargs):
            pass

        def split_documents(self, documents):
            return []

    monkeypatch.setattr(
        ingestion,
        "RecursiveCharacterTextSplitter",
        EmptySplitter,
    )

    # Prevent this test from loading any actual documents.
    class EmptyLoader:
        def __init__(self, *args, **kwargs):
            pass

        def load(self):
            from langchain_core.documents import Document
            return [Document(page_content="sample text", metadata={})]

    monkeypatch.setattr(ingestion, "UnstructuredFileLoader", EmptyLoader)
    monkeypatch.setattr(ingestion, "TextLoader", EmptyLoader)

    (documents_dir / "engineering" / "sample.md").write_text(
        "sample text",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="No document chunks"):
        ingestion.build_vector_database()

    assert marker.read_text(encoding="utf-8") == "existing index"


def test_existing_backup_stops_rebuild_without_deleting_backup(
    monkeypatch,
    tmp_path,
):
    documents_dir = tmp_path / "documents"
    department_dir = documents_dir / "engineering"
    department_dir.mkdir(parents=True)

    (department_dir / "sample.md").write_text(
        "sample engineering content",
        encoding="utf-8",
    )

    chroma_dir = tmp_path / "chroma_db"
    chroma_dir.mkdir()
    marker = chroma_dir / "existing_index.txt"
    marker.write_text("old index", encoding="utf-8")

    backup_dir = tmp_path / "chroma_db_backup"
    backup_dir.mkdir()
    backup_marker = backup_dir / "backup.txt"
    backup_marker.write_text("previous backup", encoding="utf-8")

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    class FakeSplitter:
        def __init__(self, **kwargs):
            pass

        def split_documents(self, documents):
            return documents

    class FakeLoader:
        def __init__(self, *args, **kwargs):
            pass

        def load(self):
            from langchain_core.documents import Document
            return [Document(page_content="sample text", metadata={})]

    fake_db = Mock()
    fake_db._collection.count.return_value = 1

    monkeypatch.setattr(
        ingestion,
        "RecursiveCharacterTextSplitter",
        FakeSplitter,
    )
    monkeypatch.setattr(ingestion, "UnstructuredFileLoader", FakeLoader)
    monkeypatch.setattr(ingestion, "TextLoader", FakeLoader)
    monkeypatch.setattr(ingestion.Chroma, "from_documents", Mock(return_value=fake_db))

    with pytest.raises(FileExistsError, match="Backup directory already exists"):
        ingestion.build_vector_database()

    assert marker.read_text(encoding="utf-8") == "old index"
    assert backup_marker.read_text(encoding="utf-8") == "previous backup"



def test_chroma_build_failure_preserves_existing_index(
    monkeypatch,
    tmp_path,
):
    from langchain_core.documents import Document

    documents_dir = tmp_path / "documents"
    department_dir = documents_dir / "engineering"
    department_dir.mkdir(parents=True)

    (department_dir / "sample.md").write_text(
        "sample engineering content",
        encoding="utf-8",
    )

    chroma_dir = tmp_path / "chroma_db"
    chroma_dir.mkdir()
    marker = chroma_dir / "existing_index.txt"
    marker.write_text("old index", encoding="utf-8")

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    class FakeSplitter:
        def __init__(self, **kwargs):
            pass

        def split_documents(self, documents):
            return documents

    class FakeLoader:
        def __init__(self, *args, **kwargs):
            pass

        def load(self):
            return [Document(page_content="sample text", metadata={})]

    def fail_build(**kwargs):
        raise RuntimeError("Simulated Chroma build failure")

    monkeypatch.setattr(
        ingestion,
        "RecursiveCharacterTextSplitter",
        FakeSplitter,
    )
    monkeypatch.setattr(ingestion, "UnstructuredFileLoader", FakeLoader)
    monkeypatch.setattr(ingestion, "TextLoader", FakeLoader)
    monkeypatch.setattr(ingestion.Chroma, "from_documents", fail_build)

    with pytest.raises(RuntimeError, match="Simulated Chroma build failure"):
        ingestion.build_vector_database()

    assert marker.read_text(encoding="utf-8") == "old index"
    assert not list(tmp_path.glob("chroma_db_build_*"))


def test_failed_activation_attempts_to_restore_existing_index(
    monkeypatch,
    tmp_path,
):
    from langchain_core.documents import Document

    documents_dir = tmp_path / "documents"
    department_dir = documents_dir / "engineering"
    department_dir.mkdir(parents=True)

    (department_dir / "sample.md").write_text(
        "sample engineering content",
        encoding="utf-8",
    )

    chroma_dir = tmp_path / "chroma_db"
    chroma_dir.mkdir()
    marker = chroma_dir / "existing_index.txt"
    marker.write_text("old index", encoding="utf-8")

    monkeypatch.setattr(ingestion, "DOCUMENTS_DIR", documents_dir)
    monkeypatch.setattr(ingestion, "CHROMA_DIR", chroma_dir)

    class FakeSplitter:
        def __init__(self, **kwargs):
            pass

        def split_documents(self, documents):
            return documents

    class FakeLoader:
        def __init__(self, *args, **kwargs):
            pass

        def load(self):
            return [Document(page_content="sample text", metadata={})]

    fake_db = Mock()
    fake_db._collection.count.return_value = 1

    monkeypatch.setattr(
        ingestion,
        "RecursiveCharacterTextSplitter",
        FakeSplitter,
    )
    monkeypatch.setattr(ingestion, "UnstructuredFileLoader", FakeLoader)
    monkeypatch.setattr(ingestion, "TextLoader", FakeLoader)
    monkeypatch.setattr(
        ingestion.Chroma,
        "from_documents",
        Mock(return_value=fake_db),
    )

    original_rename = Path.rename

    def fail_new_index_activation(path, target):
        path = Path(path)
        target = Path(target)

        if (
            path.name.startswith("chroma_db_build_")
            and target == chroma_dir
        ):
            raise OSError("Simulated activation failure")

        return original_rename(path, target)

    monkeypatch.setattr(Path, "rename", fail_new_index_activation)

    with pytest.raises(OSError, match="Simulated activation failure"):
        ingestion.build_vector_database()

    assert chroma_dir.exists()
    assert marker.read_text(encoding="utf-8") == "old index"
    assert not (tmp_path / "chroma_db_backup").exists()
    assert not list(tmp_path.glob("chroma_db_build_*"))
