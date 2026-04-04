import httpx

from app.services.http_check import check_http, normalize_url


class MockResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


def test_normalize_url_adds_https_scheme():
    assert normalize_url("example.com") == "https://example.com"


def test_normalize_url_keeps_existing_scheme():
    assert normalize_url("http://example.com") == "http://example.com"


def test_check_http_returns_success_result(mocker):
    mocker.patch(
        "app.services.http_check.httpx.get",
        return_value=MockResponse(200),
    )

    result = check_http("https://example.com")

    assert result["checked_url"] == "https://example.com"
    assert result["is_up"] is True
    assert result["status_code"] == 200
    assert result["response_time_ms"] is not None
    assert result["error"] is None


def test_check_http_returns_timeout_error(mocker):
    mocker.patch(
        "app.services.http_check.httpx.get",
        side_effect=httpx.TimeoutException("Timed out"),
    )

    result = check_http("https://example.com")

    assert result["checked_url"] == "https://example.com"
    assert result["is_up"] is False
    assert result["status_code"] is None
    assert result["error"] == "Request timed out"