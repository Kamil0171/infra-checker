from app.services.url_utils import normalize_url, prepare_url


def test_normalize_url_adds_https_scheme():
    assert normalize_url("example.com") == "https://example.com"


def test_prepare_url_rejects_empty_value():
    checked_url, error = prepare_url("")

    assert checked_url == ""
    assert error == "URL cannot be empty"


def test_prepare_url_rejects_spaces():
    checked_url, error = prepare_url("example .com")

    assert checked_url == ""
    assert error == "URL cannot contain spaces"


def test_prepare_url_accepts_plain_hostname():
    checked_url, error = prepare_url("example.com")

    assert checked_url == "https://example.com"
    assert error is None


def test_prepare_url_rejects_missing_hostname():
    checked_url, error = prepare_url("https:///test")

    assert checked_url == "https:///test"
    assert error == "URL must include a valid hostname"