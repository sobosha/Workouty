from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app, seed_exercise
from app.seed_exercise import EXERCISES


def get_auth_headers(client):
    email = f"test-{uuid4().hex}@example.com"
    password = "strong-password"

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

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_exercises():
    seed_exercise()

    with TestClient(app) as client:
        headers = get_auth_headers(client)
        response = client.get("/exercises", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert {exercise["name"] for exercise in EXERCISES}.issubset(
        {exercise["name"] for exercise in data}
    )
    for exercise in data:
        assert isinstance(exercise["id"], int)
        assert set(exercise) == {
            "id", "name", "description", "category", "muscle_group"
        }


def test_get_exercise_by_id():
    seed_exercise()

    with TestClient(app) as client:
        headers = get_auth_headers(client)
        list_response = client.get("/exercises", headers=headers)
        assert list_response.status_code == 200
        exercise = list_response.json()[0]

        response = client.get(f"/exercises/{exercise['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json() == exercise


def test_get_exercise_not_found():
    with TestClient(app) as client:
        headers = get_auth_headers(client)
        response = client.get("/exercises/-1", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Exercise not found"}


def test_get_exercises_without_token():
    with TestClient(app) as client:
        response = client.get("/exercises")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_exercise_by_id_without_token():
    with TestClient(app) as client:
        response = client.get("/exercises/1")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_exercises_invalid_token():
    with TestClient(app) as client:
        response = client.get(
            "/exercises",
            headers={"Authorization": "Bearer invalid-token"},
        )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_exercise_by_id_invalid_token():
    with TestClient(app) as client:
        response = client.get(
            "/exercises/1",
            headers={"Authorization": "Bearer invalid-token"},
        )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
