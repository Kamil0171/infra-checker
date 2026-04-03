# Infra Checker

Infra Checker is a lightweight web application for basic website health checks.

## Goal
The project is being built as a practical portfolio project focused on:
- DevOps basics
- Linux / system administration mindset
- HTTP/HTTPS troubleshooting
- SSL certificate checking
- automation-oriented tooling

## Planned MVP features
- check whether a website is reachable
- return HTTP status code
- measure response time
- validate SSL/TLS certificate
- calculate days until certificate expiration
- return connection-related errors

## Tech stack
- Python 3.12
- FastAPI
- Uvicorn
- httpx
- pytest
- HTML / CSS

## Project structure
```text
infra-checker/
├── app/
├── tests/
├── requirements.txt
├── README.md
├── .gitignore
├── Dockerfile
└── .github/workflows/ci.yml