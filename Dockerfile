FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install uv
COPY pyproject.toml .
# No uv.lock or full install yet since we are in bootstrap phase
# This is a minimal, single-app container placeholder
COPY . .

CMD ["uv", "run", "uvicorn", "drivers.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
