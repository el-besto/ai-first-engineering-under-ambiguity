FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install uv
COPY pyproject.toml .
# No uv.lock or full install yet since we are in bootstrap phase
# This is a minimal, single-app container placeholder
COPY . .
# CMD is explicitly overridden in docker-compose.yaml to run
# `uvicorn ...` for the API and `streamlit ...` for the UI
# using this single app footprint.
