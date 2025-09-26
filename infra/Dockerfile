FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy config/metadata and package first
COPY pyproject.toml .
COPY README.md .
COPY alembic.ini .
COPY supportdesk/ ./supportdesk/

# Install deps (editable)
RUN pip install -e .[dev]

# Non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 8000
CMD ["uvicorn", "supportdesk.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
