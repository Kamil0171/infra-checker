import httpx

from app.services.http_check import check_http


class MockResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


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


def test_check_http_rejects_space_in_url():
    result = check_http("bad url")

    assert result["checked_url"] == ""
    assert result["is_up"] is False
    assert result["status_code"] is None
    assert result["response_time_ms"] is None
    assert result["error"] == "URL cannot contain spaces"