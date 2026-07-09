import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Shared FastAPI test client.
    """
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """
    Login and return JWT Authorization headers.
    """

    response = client.post(
        "/login",
        data={
            "username": "Tony",
            "password": "password123",
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }