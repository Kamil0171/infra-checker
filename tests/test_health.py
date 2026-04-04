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


def test_check_page_renders_http_and_ssl_results(mocker):
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
    mocker.patch(
        "app.main.check_ssl",
        return_value={
            "checked_url": "https://example.com",
            "ssl_enabled": True,
            "ssl_valid": True,
            "ssl_expires_at": "2099-12-31T12:00:00+00:00",
            "ssl_days_left": 10000,
            "error": None,
        },
    )

    response = client.get("/check", params={"url": "example.com"})

    assert response.status_code == 200
    assert "https://example.com" in response.text
    assert "123.45 ms" in response.text
    assert "2099-12-31T12:00:00+00:00" in response.text
    assert "10000" in response.text