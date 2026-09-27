#!/usr/bin/env bash
# phases/20-docker-compose-from-first-principles/01-manual-orchestration-to-spec/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 20 Experiment: Compose From First Principles ==="

# Cleanup prior resources
docker rm -f dfs-manual-db dfs-manual-cache dfs-manual-web >/dev/null 2>&1 || true
docker network rm dfs-manual-net >/dev/null 2>&1 || true
docker volume rm dfs-manual-db-data >/dev/null 2>&1 || true
docker compose -f "$CODE_DIR/docker-compose.yml" down -v >/dev/null 2>&1 || true

echo "--- Part 1: Experiencing the Pain of Manual Orchestration ---"
bash "$CODE_DIR/manual_deploy.sh"

echo "Testing inter-service connectivity on manual network:"
docker exec dfs-manual-web ping -c 1 dfs-manual-cache
docker exec dfs-manual-web ping -c 1 dfs-manual-db

echo "Tearing down manual deployment..."
docker rm -f dfs-manual-db dfs-manual-cache dfs-manual-web >/dev/null
docker network rm dfs-manual-net >/dev/null
docker volume rm dfs-manual-db-data >/dev/null

echo ""
echo "--- Part 2: The Declarative Compose Translation ---"
echo "Running: docker compose up -d"
docker compose -f "$CODE_DIR/docker-compose.yml" up -d

echo ""
echo "Listing active Compose services:"
docker compose -f "$CODE_DIR/docker-compose.yml" ps

echo "Testing inter-service connectivity by SERVICE NAME:"
WEB_CID=$(docker compose -f "$CODE_DIR/docker-compose.yml" ps -q web)
docker exec "$WEB_CID" ping -c 1 cache
docker exec "$WEB_CID" ping -c 1 db

echo ""
echo "Tearing down Compose system (docker compose down -v):"
docker compose -f "$CODE_DIR/docker-compose.yml" down -v

echo ""
echo "Phase 20 Experiment Completed Successfully."
