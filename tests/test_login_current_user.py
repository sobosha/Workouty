from uuid import uuid4

from fastapi.testclient import TestClient
from app.main import app


def test_login_and_get_current_user():
    email = f"test-{uuid4().hex}@example.com"
    password = "strong-password"

    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={"email": email, "password": password},
        )
        assert register_response.status_code == 201

        login_response = client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert login_response.status_code == 200

        token_data = login_response.json()
        assert isinstance(token_data["access_token"], str)
        assert token_data["access_token"]
        assert token_data["token_type"] == "bearer"

        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

    assert response.status_code == 200
    assert response.json() == register_response.json()
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_login_wrong_password():
    email = f"test-{uuid4().hex}@example.com"

    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={"email": email, "password": "strong-password"},
        )
        assert register_response.status_code == 201

        response = client.post(
            "/auth/login",
            json={"email": email, "password": "wrong-password"},
        )

    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_login_unknown_user():
    email = f"test-{uuid4().hex}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={"email": email, "password": "strong-password"},
        )

    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_get_current_user_without_token():
    with TestClient(app) as client:
        response = client.get("/users/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_current_user_invalid_token():
    with TestClient(app) as client:
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid-token"},
        )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
