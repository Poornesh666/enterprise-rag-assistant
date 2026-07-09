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