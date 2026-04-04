import time

import httpx


def normalize_url(url: str) -> str:
    cleaned_url = url.strip()

    if not cleaned_url.startswith(("http://", "https://")):
        return f"https://{cleaned_url}"

    return cleaned_url


def check_http(url: str, timeout: float = 5.0) -> dict:
    cleaned_url = url.strip()

    if not cleaned_url:
        return {
            "checked_url": "",
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error": "URL cannot be empty",
        }

    checked_url = normalize_url(cleaned_url)
    start_time = time.perf_counter()

    try:
        response = httpx.get(
            checked_url,
            timeout=timeout,
            follow_redirects=True,
        )
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return {
            "checked_url": checked_url,
            "is_up": True,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "error": None,
        }

    except httpx.TimeoutException:
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": "Request timed out",
        }

    except httpx.ConnectError:
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": "Could not connect to the host",
        }

    except httpx.InvalidURL:
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error": "Invalid URL format",
        }

    except httpx.RequestError as exc:
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": f"Request error: {exc.__class__.__name__}",
        }