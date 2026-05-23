FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "PYTHONPATH=/app alembic upgrade head && PYTHONPATH=/app python scripts/seed_demo.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
