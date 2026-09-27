#!/usr/bin/env bash
set -euo pipefail

echo "Stopping all NoSQL scratch containers..."

if command -v docker-compose >/dev/null 2>&1; then
    docker-compose --profile all down
elif docker compose version >/dev/null 2>&1; then
    docker compose --profile all down
else
    echo "Stopping containers by name pattern..."
    docker stop $(docker ps -q --filter "name=nosql-") 2>/dev/null || true
fi

echo "All NoSQL laboratory containers stopped."
