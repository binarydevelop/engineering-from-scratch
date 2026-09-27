#!/usr/bin/env bash
# Lab Bootstrap Script
# Boots Tier 1 local production environment (Docker Compose) or standalone services

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================================="
echo "Starting Production SRE & Observability Lab (Tier 1)"
echo "=========================================================="

cd "${REPO_ROOT}"

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Check if Docker is running
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    echo "Docker engine is active. Launching stack via Docker Compose..."
    docker compose up -d --build
    echo ""
    echo "Waiting for services to become healthy..."
    sleep 5
    echo ""
    echo "Stack status:"
    docker compose ps
    echo ""
    echo "Access Endpoints:"
    echo "  - API Gateway:           http://localhost:8000"
    echo "  - Checkout Service:      http://localhost:8001"
    echo "  - Inventory Service:     http://localhost:8002"
    echo "  - Payment Service:       http://localhost:8003"
    echo "  - Prometheus Web UI:     http://localhost:9090"
    echo "  - Alertmanager Web UI:   http://localhost:9093"
    echo "  - Grafana Dashboards:    http://localhost:3000 (admin / admin)"
    echo "  - OpenTelemetry OTLP:    localhost:4317 (gRPC) / localhost:4318 (HTTP)"
else
    echo "Docker is not running or unavailable. You can run Python services locally using:"
    echo "  make run-local-services"
fi

echo "=========================================================="
echo "Lab startup complete."
