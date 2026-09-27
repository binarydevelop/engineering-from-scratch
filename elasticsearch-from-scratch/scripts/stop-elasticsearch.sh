#!/usr/bin/env bash
# ==============================================================================
# stop-elasticsearch.sh - Gracefully shut down Elasticsearch lab containers
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "Stopping Elasticsearch single-node containers..."
docker compose -f docker-compose.yml down --remove-orphans || true

echo "Stopping Elasticsearch cluster containers..."
docker compose -f docker-compose.cluster.yml down --remove-orphans || true

echo "All Elasticsearch lab containers stopped."
