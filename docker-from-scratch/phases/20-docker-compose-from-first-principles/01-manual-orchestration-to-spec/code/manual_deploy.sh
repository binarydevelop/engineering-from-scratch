#!/usr/bin/env bash
# manual_deploy.sh
# Demonstrates the pain of manual multi-container orchestration.
set -euo pipefail

echo "=== 1. Creating Private Network ==="
docker network create dfs-manual-net

echo "=== 2. Creating Persistent Volume ==="
docker volume create dfs-manual-db-data

echo "=== 3. Launching Database (Postgres) ==="
docker run -d --name dfs-manual-db \
    --network dfs-manual-net \
    -v dfs-manual-db-data:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=secret123 \
    postgres:16-alpine

echo "=== 4. Launching Cache (Redis) ==="
docker run -d --name dfs-manual-cache \
    --network dfs-manual-net \
    redis:7-alpine

echo "=== 5. Launching Web Service ==="
docker run -d --name dfs-manual-web \
    --network dfs-manual-net \
    -p 8081:8000 \
    -e REDIS_HOST=dfs-manual-cache \
    -e DB_HOST=dfs-manual-db \
    alpine:latest sleep 60

echo "All 3 services deployed manually."
