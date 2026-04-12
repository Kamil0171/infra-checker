from dataclasses import dataclass
from functools import lru_cache
import os

from dotenv import load_dotenv

load_dotenv()


def _get_float_env(name: str, default: float) -> float:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        parsed_value = float(value)
    except ValueError:
        return default

    if parsed_value <= 0:
        return default

    return parsed_value


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    request_timeout: float


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Infra Checker"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        request_timeout=_get_float_env("REQUEST_TIMEOUT", 5.0),
    )