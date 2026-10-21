
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document

import app.rag.retriever as retriever


@pytest.fixture
def mock_vectordb(monkeypatch):
    """Replace the real ChromaDB instance with a mock."""
    fake_db = Mock()

    fake_db.similarity_search.return_value = [
        Document(
            page_content="Sample test document",
            metadata={"role": "engineering", "category": "engineering"},
        )
    ]

    monkeypatch.setattr(retriever, "vectordb", fake_db)
    monkeypatch.setattr(retriever.settings, "top_k", 5)

    return fake_db


def test_employee_retrieval_filters_general_documents(mock_vectordb):
    retriever.retrieve_documents("company policy", "employee")

    mock_vectordb.similarity_search.assert_called_once_with(
        "company policy",
        k=5,
        filter={"category": "general"},
    )


def test_engineering_retrieval_filters_engineering_documents(mock_vectordb):
    retriever.retrieve_documents("deployment strategy", "engineering")

    mock_vectordb.similarity_search.assert_called_once_with(
        "deployment strategy",
        k=5,
        filter={"role": "engineering"},
    )


def test_finance_retrieval_filters_finance_documents(mock_vectordb):
    retriever.retrieve_documents("quarterly expenses", "finance")

    mock_vectordb.similarity_search.assert_called_once_with(
        "quarterly expenses",
        k=5,
        filter={"role": "finance"},
    )


def test_executive_retrieval_searches_all_documents(mock_vectordb):
    retriever.retrieve_documents("company strategy", "c-levelexecutives")

    mock_vectordb.similarity_search.assert_called_once_with(
        "company strategy",
        k=5,
    )


def test_role_is_case_insensitive(mock_vectordb):
    retriever.retrieve_documents("deployment strategy", "ENGINEERING")

    mock_vectordb.similarity_search.assert_called_once_with(
        "deployment strategy",
        k=5,
        filter={"role": "engineering"},
    )


def test_executive_retrieval_uses_fallback_when_initial_search_is_empty(
    mock_vectordb,
):
    mock_vectordb.similarity_search.side_effect = [
        [],
        [
            Document(
                page_content="Fallback document",
                metadata={"role": "engineering"},
            )
        ],
    ]

    docs = retriever.retrieve_documents(
        "company strategy",
        "c-levelexecutives",
    )

    assert len(docs) == 1
    assert docs[0].page_content == "Fallback document"

    assert mock_vectordb.similarity_search.call_count == 2

    mock_vectordb.similarity_search.assert_any_call(
        "company strategy",
        k=5,
    )

    mock_vectordb.similarity_search.assert_any_call(
        "company strategy",
        k=5,
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


@pytest.mark.parametrize(
    "role",
    ["employee", "engineering", "finance"],
)
def test_retrieval_returns_empty_list_when_no_documents_found(
    mock_vectordb,
    role,
):
    mock_vectordb.similarity_search.return_value = []

    docs = retriever.retrieve_documents(
        "query with no matching documents",
        role,
    )

    assert docs == []
