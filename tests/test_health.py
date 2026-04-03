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


def test_check_page_returns_submitted_url():
    response = client.get("/check", params={"url": "https://example.com"})

    assert response.status_code == 200
    assert "https://example.com" in response.text
    assert "Form submission works correctly" in response.text