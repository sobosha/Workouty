from fastapi.testclient import TestClient
from app.main import app

def test_health_db():
    with TestClient(app) as client:
        response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}