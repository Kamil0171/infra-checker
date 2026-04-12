from app.services.ssl_check import check_ssl, parse_certificate_expiry


class FakeSocket:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeSSLSocket:
    def __init__(self, certificate: dict):
        self.certificate = certificate

    def getpeercert(self):
        return self.certificate

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeSSLContext:
    def __init__(self, certificate: dict):
        self.certificate = certificate

    def wrap_socket(self, sock, server_hostname):
        return FakeSSLSocket(self.certificate)


def test_parse_certificate_expiry_returns_datetime():
    expiry = parse_certificate_expiry("Dec 31 12:00:00 2099 GMT")

    assert expiry.year == 2099
    assert expiry.month == 12
    assert expiry.day == 31


def test_check_ssl_skips_non_https_url():
    result = check_ssl("http://example.com")

    assert result["ssl_enabled"] is False
    assert result["ssl_valid"] is None
    assert result["ssl_expires_at"] is None
    assert result["ssl_days_left"] is None
    assert result["error"] is None


def test_check_ssl_returns_validation_error_for_bad_url():
    result = check_ssl("bad url")

    assert result["checked_url"] == ""
    assert result["ssl_enabled"] is None
    assert result["ssl_valid"] is None
    assert result["ssl_expires_at"] is None
    assert result["ssl_days_left"] is None
    assert result["error"] == "URL cannot contain spaces"


def test_check_ssl_returns_certificate_data(mocker):
    certificate = {
        "notAfter": "Dec 31 12:00:00 2099 GMT",
    }

    mocker.patch(
        "app.services.ssl_check.socket.create_connection",
        return_value=FakeSocket(),
    )
    mocker.patch(
        "app.services.ssl_check.ssl.create_default_context",
        return_value=FakeSSLContext(certificate),
    )

    result = check_ssl("https://example.com")

    assert result["checked_url"] == "https://example.com"
    assert result["ssl_enabled"] is True
    assert result["ssl_valid"] is True
    assert result["ssl_expires_at"] is not None
    assert result["ssl_days_left"] is not None
    assert result["error"] is None