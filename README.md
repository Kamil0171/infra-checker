# Infra Checker
[![CI](https://github.com/Kamil0171/infra-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/Kamil0171/infra-checker/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-web%20app-009688)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![Status](https://img.shields.io/badge/status-v1.0.0-success)

Infra Checker is a lightweight web application for checking basic website health, HTTP response details, and SSL/TLS certificate status.

## Goal

This project is focused on:
- DevOps basics
- Linux / system administration mindset
- HTTP/HTTPS troubleshooting
- SSL certificate checking
- automation-oriented tooling

## Current features

- website availability check
- HTTP status code check
- response time measurement
- SSL/TLS certificate validation
- certificate expiration date check
- days left until certificate expiration
- basic frontend with dynamic result rendering
- JSON API endpoint for checks
- centralized application settings
- environment-based timeout configuration
- basic application logging
- automated tests with pytest
- linting with Ruff
- Docker support
- GitHub Actions CI

## Tech stack

- Python 3.12
- FastAPI
- Uvicorn
- httpx
- pytest
- Ruff
- HTML / CSS / JavaScript
- Docker
- GitHub Actions

## Project structure

```text
infra-checker/
├── app/
│   ├── config.py
│   ├── logging_config.py
│   ├── main.py
│   ├── schemas.py
│   ├── services/
│   │   ├── http_check.py
│   │   ├── ssl_check.py
│   │   └── url_utils.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── app.js
├── tests/
│   ├── test_health.py
│   ├── test_http_check.py
│   ├── test_ssl_check.py
│   └── test_url_utils.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── pyproject.toml
├── .env.example
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Running locally

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/
```

## Development setup

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run linting:

```bash
ruff check .
```

Run tests:

```bash
python -m pytest
```

## Environment configuration

Example environment configuration is provided in `.env.example`:

```env
APP_NAME=Infra Checker
APP_VERSION=1.0.0
REQUEST_TIMEOUT=5.0
LOG_LEVEL=INFO
```

## Running with Docker

Build the image:

```bash
docker build -t infra-checker .
```

Run the container:

```bash
docker run --rm -p 8000:8000 infra-checker
```

Open in browser:

```
http://127.0.0.1:8000/
```

## API endpoints

### Health check

```
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Website check API

```
GET /api/check?url=example.com
```

Example response:

```json
{
  "submitted_url": "example.com",
  "http": {
    "checked_url": "https://example.com",
    "is_up": true,
    "status_code": 200,
    "response_time_ms": 123.45,
    "error": null
  },
  "ssl": {
    "checked_url": "https://example.com",
    "ssl_enabled": true,
    "ssl_valid": true,
    "ssl_expires_at": "2099-12-31T12:00:00+00:00",
    "ssl_days_left": 9999,
    "error": null
  }
}
```
