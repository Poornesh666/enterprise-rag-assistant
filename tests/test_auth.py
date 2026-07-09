def test_login_success(client):
    response = client.post(
        "/login",
        data={
            "username": "Tony",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
def test_login_invalid_password(client):
    response = client.post(
        "/login",
        data={
            "username": "Tony",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    
def test_register_success(client):
    response = client.post(
        "/register",
        json={
            "username": "pytest_user",
            "password": "password123",
            "role": "engineering",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "pytest_user"
    assert data["role"] == "engineering"
    
def test_register_duplicate_username(client):
    response = client.post(
        "/register",
        json={
            "username": "Tony",
            "password": "password123",
            "role": "engineering",
        },
    )

    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == "Username already exists."
    
def test_login_nonexistent_user(client):
    response = client.post(
        "/login",
        data={
            "username": "nonexistent_user",
            "password": "password123",
        },
    )

    assert response.status_code == 401