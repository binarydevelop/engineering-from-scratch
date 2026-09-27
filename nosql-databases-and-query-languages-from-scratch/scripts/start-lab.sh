#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1:-all}"

echo "Starting NoSQL database laboratory profile: $PROFILE"

if command -v docker-compose >/dev/null 2>&1; then
    docker-compose --profile "$PROFILE" up -d
elif docker compose version >/dev/null 2>&1; then
    docker compose --profile "$PROFILE" up -d
else
    echo "Error: Neither docker-compose nor docker compose plugin found!"
    exit 1
fi

echo "Containers launched. Waiting for services to be ready..."
sleep 3
docker ps --filter "name=nosql-"
