def test_chat_success(client, auth_headers):
    response = client.post(
        "/chat",
        headers=auth_headers,
        json={
            "message": "What is the deployment strategy?"
        },
    )

    assert response.status_code == 200

    data = response.json()
    
    assert data["username"] == "Tony"
    assert data["role"] == "engineering"
    assert "response" in data
    assert data["query"] == "What is the deployment strategy?"
    
    
def test_chat_without_token_is_rejected(client):
    response = client.post(
        "/chat",
        json={"message": "What is the deployment strategy?"},
    )

    assert response.status_code == 401


def test_chat_with_invalid_token_is_rejected(client):
    response = client.post(
        "/chat",
        headers={"Authorization": "Bearer invalid-token"},
        json={"message": "What is the deployment strategy?"},
    )

    assert response.status_code == 401


def test_client_cannot_override_authenticated_role(
    client,
    auth_headers,
    monkeypatch,
):
    import app.api.chat as chat_module

    captured_roles = []

    def fake_retrieve_documents(query: str, role: str):
        captured_roles.append(role)

        # Return a minimal document so the endpoint can continue.
        from langchain_core.documents import Document

        return [
            Document(
                page_content="Engineering deployment policy.",
                metadata={"role": "engineering"},
            )
        ]

    monkeypatch.setattr(
        chat_module,
        "retrieve_documents",
        fake_retrieve_documents,
    )
    monkeypatch.setattr(
        chat_module,
        "generate_response",
        lambda prompt: "Use the approved engineering deployment process.",
    )

    response = client.post(
        "/chat",
        headers=auth_headers,
        json={
            "message": "What is the deployment strategy?",
            "role": "c-levelexecutives",
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "engineering"
    assert captured_roles == ["engineering"]
