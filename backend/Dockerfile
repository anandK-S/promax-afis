# ========================================
# Pro-Max AFIS - Backend Dockerfile
# ========================================
# Multi-stage build for optimization
# Base: Python 3.11-slim

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt requirements-dev.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOME=/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create application directory
WORKDIR $APP_HOME

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p logs ml-models data uploads && \
    chown -R appuser:appuser logs ml-models data uploads

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]