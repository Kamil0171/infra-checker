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


def test_check_page_renders_http_result(mocker):
    mocker.patch(
        "app.main.check_http",
        return_value={
            "checked_url": "https://example.com",
            "is_up": True,
            "status_code": 200,
            "response_time_ms": 123.45,
            "error": None,
        },
    )

    response = client.get("/check", params={"url": "example.com"})

    assert response.status_code == 200
    assert "example.com" in response.text
    assert "https://example.com" in response.text
    assert "200" in response.text
    assert "123.45 ms" in response.text