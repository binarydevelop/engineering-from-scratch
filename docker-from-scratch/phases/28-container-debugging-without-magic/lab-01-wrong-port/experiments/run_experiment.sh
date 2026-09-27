#!/usr/bin/env bash
# phases/28-container-debugging-without-magic/lab-01-wrong-port/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 28 Lab 01: Wrong Port Mismatch ==="

# Cleanup prior state
docker compose -f "$CODE_DIR/docker-compose.yml" down -v >/dev/null 2>&1 || true
docker compose -f "$CODE_DIR/docker-compose.fixed.yml" down -v >/dev/null 2>&1 || true

echo "Step 1: Starting the BROKEN stack..."
docker compose -f "$CODE_DIR/docker-compose.yml" up -d
sleep 2

echo "Step 2: Testing connection: curl http://localhost:8080 (Expect Failure)"
set +e
curl -s --connect-timeout 2 http://localhost:8080
FAIL_EXIT=$?
set -e
echo "Exit code: $FAIL_EXIT (Connection failed!)"

echo ""
echo "Step 3: Systematic Diagnostic Flow:"
echo "a. Is the container running?"
docker compose -f "$CODE_DIR/docker-compose.yml" ps
echo "b. What do the application logs say?"
docker compose -f "$CODE_DIR/docker-compose.yml" logs web
echo "c. What port is the container mapping?"
docker compose -f "$CODE_DIR/docker-compose.yml" port web 3000
echo "--> DIAGNOSIS: App is listening on port 8000, but Compose mapped host:8080 to container:3000!"

echo ""
echo "Step 4: Applying FIX (switching to docker-compose.fixed.yml)..."
docker compose -f "$CODE_DIR/docker-compose.yml" down >/dev/null
docker compose -f "$CODE_DIR/docker-compose.fixed.yml" up -d
sleep 2

echo "Step 5: Testing connection after fix:"
curl -s http://localhost:8080
echo "--> SUCCESS: Bug resolved without magic!"

# Cleanup
docker compose -f "$CODE_DIR/docker-compose.fixed.yml" down >/dev/null

echo ""
echo "Lab 01 Completed Successfully."
