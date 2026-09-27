#!/usr/bin/env bash
# phases/28-container-debugging-without-magic/lab-03-missing-env/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 28 Lab 03: Missing Environment Variable ==="

# Cleanup prior state
docker compose -f "$CODE_DIR/docker-compose.yml" down -v >/dev/null 2>&1 || true
docker compose -f "$CODE_DIR/docker-compose.fixed.yml" down -v >/dev/null 2>&1 || true

echo "Step 1: Launching BROKEN Compose stack..."
docker compose -f "$CODE_DIR/docker-compose.yml" up -d
sleep 1

echo ""
echo "Step 2: Inspecting container state (docker compose ps -a):"
docker compose -f "$CODE_DIR/docker-compose.yml" ps -a

echo ""
echo "Step 3: Checking process logs for crash trace:"
docker compose -f "$CODE_DIR/docker-compose.yml" logs api
echo "--> DIAGNOSIS: Python threw KeyError: 'API_SECRET_KEY' because env var is unset."

echo ""
echo "Step 4: Launching FIXED Compose stack with injected environment variable..."
docker compose -f "$CODE_DIR/docker-compose.yml" down >/dev/null
docker compose -f "$CODE_DIR/docker-compose.fixed.yml" up
docker compose -f "$CODE_DIR/docker-compose.fixed.yml" down >/dev/null

echo ""
echo "Lab 03 Completed Successfully."
