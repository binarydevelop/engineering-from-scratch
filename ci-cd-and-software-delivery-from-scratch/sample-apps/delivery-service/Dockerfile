# syntax=docker/dockerfile:1.4
# Multi-stage secure build for Delivery Service (Phases 61, 62)

# --- Stage 1: Build & Dependency Resolution ---
FROM python:3.12.5-slim AS builder

WORKDIR /build

# Ensure security updates and compile tools if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# In sample app, requirements are self-contained or pinned
RUN pip install --no-cache-dir --user -r requirements.txt || true


# --- Stage 2: Minimal Distroless / Hardened Runtime ---
FROM python:3.12.5-slim AS runtime

# Label metadata for OCI image specification
LABEL org.opencontainers.image.title="delivery-service" \
      org.opencontainers.image.description="Sample Backend Delivery Service for CI/CD Curriculum" \
      org.opencontainers.image.authors="binarydevelop/engineering-from-scratch" \
      org.opencontainers.image.source="https://github.com/binarydevelop/ci-cd-and-software-delivery-from-scratch"

# Create unprivileged system user and group (Least Privilege - Phase 62)
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy application files
COPY --chown=appuser:appgroup app.py /app/app.py
COPY --chown=appuser:appgroup db/ /app/db/

# Switch to unprivileged user
USER appuser

# Environment variables (Twelve-Factor App)
ENV PORT=8080 \
    HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

EXPOSE 8080

# Health check using native Python standard library
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health/liveness')" || exit 1

ENTRYPOINT ["python3", "app.py"]
