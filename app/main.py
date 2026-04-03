from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Infra Checker", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <html>
        <head>
            <title>Infra Checker</title>
        </head>
        <body>
            <h1>Infra Checker</h1>
            <p>Application is running.</p>
            <p>Health endpoint: /health</p>
        </body>
    </html>
    """