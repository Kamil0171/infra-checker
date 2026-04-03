from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page_returns_200():
    response = client.get("/")

    assert response.status_code == 200
    assert "Infra Checker" in response.text