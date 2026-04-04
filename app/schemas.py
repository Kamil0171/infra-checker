from pydantic import BaseModel


class HttpCheckResult(BaseModel):
    checked_url: str
    is_up: bool
    status_code: int | None = None
    response_time_ms: float | None = None
    error: str | None = None


class SSLCheckResult(BaseModel):
    checked_url: str
    ssl_enabled: bool | None = None
    ssl_valid: bool | None = None
    ssl_expires_at: str | None = None
    ssl_days_left: int | None = None
    error: str | None = None


class CheckResponse(BaseModel):
    submitted_url: str
    http: HttpCheckResult
    ssl: SSLCheckResult