from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.schemas import CheckResponse, HttpCheckResult, SSLCheckResult
from app.services.http_check import check_http
from app.services.ssl_check import check_ssl

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def build_check_response(url: str) -> CheckResponse:
    cleaned_url = url.strip()

    http_result = HttpCheckResult(**check_http(cleaned_url))
    ssl_result = SSLCheckResult(**check_ssl(cleaned_url))

    return CheckResponse(
        submitted_url=cleaned_url,
        http=http_result,
        ssl=ssl_result,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "submitted_url": "",
            "result": None,
        },
    )


@app.get("/check", response_class=HTMLResponse)
def check_page(request: Request, url: str = Query(..., min_length=1)):
    result = build_check_response(url)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "submitted_url": result.submitted_url,
            "result": result,
        },
    )


@app.get("/api/check", response_model=CheckResponse)
def api_check(url: str = Query(..., min_length=1)):
    return build_check_response(url)