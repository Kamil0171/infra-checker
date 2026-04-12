from datetime import datetime, timezone
import socket
import ssl
from urllib.parse import urlsplit

from app.config import get_settings
from app.services.http_check import normalize_url


def parse_certificate_expiry(not_after: str) -> datetime:
    expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
    return expiry.replace(tzinfo=timezone.utc)


def check_ssl(url: str, timeout: float | None = None) -> dict:
    settings = get_settings()
    effective_timeout = timeout if timeout is not None else settings.request_timeout

    cleaned_url = url.strip()

    if not cleaned_url:
        return {
            "checked_url": "",
            "ssl_enabled": None,
            "ssl_valid": None,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "URL cannot be empty",
        }

    checked_url = normalize_url(cleaned_url)

    try:
        parsed_url = urlsplit(checked_url)
    except ValueError:
        return {
            "checked_url": checked_url,
            "ssl_enabled": None,
            "ssl_valid": None,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "Invalid URL format",
        }

    if parsed_url.scheme != "https":
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
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "Could not determine hostname from URL",
        }

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=effective_timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                certificate = ssl_sock.getpeercert()

        if not certificate:
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

        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": expires_at > now_utc,
            "ssl_expires_at": expires_at.isoformat(),
            "ssl_days_left": days_left,
            "error": None,
        }

    except ssl.SSLCertVerificationError:
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "Certificate verification failed",
        }

    except ssl.SSLError as exc:
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": f"TLS error: {exc.__class__.__name__}",
        }

    except socket.timeout:
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "TLS connection timed out",
        }

    except socket.gaierror:
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": "DNS resolution failed",
        }

    except OSError as exc:
        return {
            "checked_url": checked_url,
            "ssl_enabled": True,
            "ssl_valid": False,
            "ssl_expires_at": None,
            "ssl_days_left": None,
            "error": f"Connection error: {exc.__class__.__name__}",
        }