# Multi-stage build for Python backend
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# Final stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user first
RUN useradd -m -u 1000 monolith && \
    mkdir -p /app/data /app/models && \
    chown -R monolith:monolith /app

# Copy Python dependencies from builder to user's local directory
COPY --from=builder --chown=monolith:monolith /root/.local /home/monolith/.local

# Copy application code
COPY --chown=monolith:monolith ./app ./app

# Set environment variables
ENV PATH=/home/monolith/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    MODELS_DIR=/app/models \
    DATA_DIR=/app/data

USER monolith

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
