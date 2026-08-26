FROM python:3.12-slim

WORKDIR /app

# psycopg[binary] and bcrypt need build tools on some base images; keep slim
# but make sure the wheel install doesn't fail on a bare python:slim image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Apply migrations then start the API. Compose's `depends_on: condition:
# service_healthy` ensures db/redis are up first; this entrypoint handles the
# "db is up but not yet accepting the hirly role/schema" race on cold start.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
