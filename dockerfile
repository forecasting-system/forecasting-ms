# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential libatlas-base-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to path
ENV PATH="/root/.local/bin:$PATH"

# Copy only relevant files first for better layer caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies (no dev deps)
RUN poetry install --no-root --without dev

# Copy the rest of the code
COPY . /app/

# Expose port (optional, define if you want to run standalone outside Docker Compose)
EXPOSE 8000

# Run the app
CMD ["poetry", "run", "uvicorn", "app.entrypoints.main:app", "--host", "0.0.0.0", "--port", "8000"]
