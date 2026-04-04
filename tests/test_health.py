from fastapi.testclient import TestClient

from app.main import app
from app.schemas import CheckResponse, HttpCheckResult, SSLCheckResult

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
        "app.main.build_check_response",
        return_value=CheckResponse(
            submitted_url="example.com",
            http=HttpCheckResult(
                checked_url="https://example.com",
                is_up=True,
                status_code=200,
                response_time_ms=123.45,
                error=None,
            ),
            ssl=SSLCheckResult(
                checked_url="https://example.com",
                ssl_enabled=True,
                ssl_valid=True,
                ssl_expires_at="2099-12-31T12:00:00+00:00",
                ssl_days_left=10000,
                error=None,
            ),
        ),
    )

    response = client.get("/check", params={"url": "example.com"})

    assert response.status_code == 200
    assert "https://example.com" in response.text
    assert "123.45 ms" in response.text
    assert "2099-12-31T12:00:00+00:00" in response.text
    assert "10000" in response.text


def test_api_check_returns_json_result(mocker):
    mocker.patch(
        "app.main.build_check_response",
        return_value=CheckResponse(
            submitted_url="example.com",
            http=HttpCheckResult(
                checked_url="https://example.com",
                is_up=True,
                status_code=200,
                response_time_ms=150.5,
                error=None,
            ),
            ssl=SSLCheckResult(
                checked_url="https://example.com",
                ssl_enabled=True,
                ssl_valid=True,
                ssl_expires_at="2099-12-31T12:00:00+00:00",
                ssl_days_left=9999,
                error=None,
            ),
        ),
    )

    response = client.get("/api/check", params={"url": "example.com"})

    assert response.status_code == 200

    data = response.json()
    assert data["submitted_url"] == "example.com"
    assert data["http"]["checked_url"] == "https://example.com"
    assert data["http"]["status_code"] == 200
    assert data["ssl"]["ssl_valid"] is True
    assert data["ssl"]["ssl_days_left"] == 9999