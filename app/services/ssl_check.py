import logging
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlsplit

from app.config import get_settings
from app.services.url_utils import prepare_url

logger = logging.getLogger(__name__)


def parse_certificate_expiry(not_after: str) -> datetime:
    expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
    return expiry.replace(tzinfo=timezone.utc)


def check_ssl(url: str, timeout: float | None = None) -> dict:
    settings = get_settings()
    effective_timeout = timeout if timeout is not None else settings.request_timeout

    checked_url, validation_error = prepare_url(url)

    if validation_error:
        logger.warning("SSL check validation failed for url=%r: %s", url, validation_error)
        return {
            "checked_url": checked_url,
            "ssl_enabled": None,
            "ssl_valid": None,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": validation_error,
        }

    parsed_url = urlsplit(checked_url)

    if parsed_url.scheme != "https":
        logger.info("Skipping SSL check for non-HTTPS url=%s", checked_url)
        return {
            "checked_url": checked_url,
            "ssl_enabled": False,
            "ssl_valid": None,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": None,
        }

    hostname = parsed_url.hostname
    port = parsed_url.port or 443

    if not hostname:
        logger.warning("SSL check could not determine hostname for url=%s", checked_url)
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "URL must include a valid hostname",
        }

    context = ssl.create_default_context()

    try:
        logger.info("Starting SSL check for %s", checked_url)
        with socket.create_connection((hostname, port), timeout=effective_timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                certificate = ssl_sock.getpeercert()

        if not certificate:
            logger.warning("No certificate returned for %s", checked_url)
            return {
                "checked_url": checked_url,
                "ssl_enabled": True,
                "ssl_valid": False,
                "ssl_expires_at": None,
                "ssl_days_left": None,
                "error": "No certificate was provided by the server",
            }

        not_after = certificate.get("notAfter")
        if not not_after:
            logger.warning("Certificate expiry missing for %s", checked_url)
            return {
                "checked_url": checked_url,
                "ssl_enabled": True,
                "ssl_valid": False,
                "ssl_expires_at": None,
                "ssl_days_left": None,
                "error": "Certificate expiration date is unavailable",
            }

        expires_at = parse_certificate_expiry(not_after)
        now_utc = datetime.now(timezone.utc)
        days_left = (expires_at - now_utc).days

        logger.info(
            "SSL check completed for %s: valid=%s days_left=%s",
            checked_url,
            expires_at > now_utc,
            days_left,
        )

        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": expires_at > now_utc,
            "ssl_expires_at": expires_at.isoformat(),
            "ssl_days_left": days_left,
            "error": None,
        }

    except ssl.SSLCertVerificationError:
        logger.warning("SSL certificate verification failed for %s", checked_url)
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "Certificate verification failed",
        }

    except ssl.SSLError as exc:
        logger.warning("SSL error for %s: %s", checked_url, exc.__class__.__name__)
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": f"TLS error: {exc.__class__.__name__}",
        }

    except socket.timeout:
        logger.warning("SSL timeout for %s", checked_url)
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "TLS connection timed out",
        }

    except socket.gaierror:
        logger.warning("SSL DNS resolution failed for %s", checked_url)
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "DNS resolution failed",
        }

    except OSError as exc:
        logger.warning("SSL connection error for %s: %s", checked_url, exc.__class__.__name__)
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": f"Connection error: {exc.__class__.__name__}",
        }