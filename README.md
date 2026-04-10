# Infra Checker
[![CI](https://github.com/Kamil0171/infra-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/Kamil0171/infra-checker/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-web%20app-009688)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![Status](https://img.shields.io/badge/status-MVP-success)

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
- automated tests with pytest
- Docker support
- GitHub Actions CI

## Tech stack

- Python 3.12
- FastAPI
- Uvicorn
- httpx
- pytest
- HTML / CSS / JavaScript
- Docker
- GitHub Actions

## Project structure

```text
infra-checker/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── services/
│   │   ├── http_check.py
│   │   └── ssl_check.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── app.js
├── tests/
│   ├── test_health.py
│   ├── test_http_check.py
│   └── test_ssl_check.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md