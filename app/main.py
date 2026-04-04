from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.http_check import check_http

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Infra Checker", version="0.1.0")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


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
    cleaned_url = url.strip()
    http_result = check_http(cleaned_url)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "submitted_url": cleaned_url,
            "result": http_result,
        },
    )