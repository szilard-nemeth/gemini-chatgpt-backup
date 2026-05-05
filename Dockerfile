FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    ca-certificates \
    nodejs \
    npm \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Install single-file-cli
RUN npm install -g single-file-cli

WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Install Playwright browsers
RUN playwright install chromium

# Copy project
COPY . /app

CMD ["poetry", "run", "python", "publix_export_playwright_structured.py"]
