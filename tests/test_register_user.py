from uuid import uuid4

from fastapi.testclient import TestClient
from app.main import app


def test_register_user():
    email = f"test-{uuid4().hex}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "strong-password",
            },
        )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == email
    assert isinstance(data["id"], int)
    assert "created_at" in data
    assert "password" not in data
    assert "password_hash" not in data
    
def test_register_user_duplicate():
    email = f"test-{uuid4().hex}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "strong-password",
            },
        )
        
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "strong-password",
        },
    )
    

    assert response.status_code == 409
    
def test_register_user_invalid_email():
    email = "not-an-email"

    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "strong-password",
            },
        )
    

    assert response.status_code == 422