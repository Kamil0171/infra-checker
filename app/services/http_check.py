import logging
import time

import httpx

from app.config import get_settings
from app.services.url_utils import prepare_url

logger = logging.getLogger(__name__)


def check_http(url: str, timeout: float | None = None) -> dict:
    settings = get_settings()
    effective_timeout = timeout if timeout is not None else settings.request_timeout

    checked_url, validation_error = prepare_url(url)

    if validation_error:
        logger.warning("HTTP check validation failed for url=%r: %s", url, validation_error)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error": validation_error,
        }

    start_time = time.perf_counter()

    try:
        logger.info("Starting HTTP check for %s", checked_url)
        response = httpx.get(
            checked_url,
            timeout=effective_timeout,
            follow_redirects=True,
        )
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "HTTP check completed for %s with status=%s in %.2f ms",
            checked_url,
            response.status_code,
            response_time_ms,
        )

        return {
            "checked_url": checked_url,
            "is_up": True,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "error": None,
        }

    except httpx.TimeoutException:
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.warning("HTTP timeout for %s after %.2f ms", checked_url, response_time_ms)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": "Request timed out",
        }

    except httpx.ConnectError:
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.warning("HTTP connect error for %s after %.2f ms", checked_url, response_time_ms)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": "Could not connect to the host",
        }

    except httpx.InvalidURL:
        logger.warning("HTTP invalid URL for %s", checked_url)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error": "Invalid URL format",
        }

    except httpx.RequestError as exc:
        response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.exception("HTTP request error for %s: %s", checked_url, exc.__class__.__name__)
        return {
            "checked_url": checked_url,
            "is_up": False,
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": f"Request error: {exc.__class__.__name__}",
        }