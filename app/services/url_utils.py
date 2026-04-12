from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    cleaned_url = url.strip()

    if not cleaned_url.startswith(("http://", "https://")):
        return f"https://{cleaned_url}"

    return cleaned_url


def prepare_url(url: str) -> tuple[str, str | None]:
    cleaned_url = url.strip()

    if not cleaned_url:
        return "", "URL cannot be empty"

    if " " in cleaned_url:
        return "", "URL cannot contain spaces"

    normalized_url = normalize_url(cleaned_url)

    try:
        parsed_url = urlsplit(normalized_url)
    except ValueError:
        return normalized_url, "Invalid URL format"

    if parsed_url.scheme not in {"http", "https"}:
        return normalized_url, "Only http and https URLs are supported"

    if not parsed_url.hostname:
        return normalized_url, "URL must include a valid hostname"

    return normalized_url, None