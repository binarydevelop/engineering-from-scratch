#!/usr/bin/env bash
# phases/28-container-debugging-without-magic/lab-04-localhost-trap/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 28 Lab 04: The Localhost Trap ==="

# Cleanup prior containers
docker rm -f dfs-lab04-broken dfs-lab04-fixed >/dev/null 2>&1 || true

echo "Step 1: Starting container with server bound to 127.0.0.1 (-p 8080:8080)..."
docker run -d --name dfs-lab04-broken -p 8080:8080 \
    -v "$CODE_DIR/server_broken.py":/app.py \
    python:3.11-slim python3 /app.py >/dev/null
sleep 1

echo "Step 2: Testing connection from HOST: curl http://localhost:8080 (Expect Failure):"
set +e
curl -s --connect-timeout 2 http://localhost:8080
FAIL_EXIT=$?
set -e
echo "Exit Code: $FAIL_EXIT (Connection failed!)"

echo ""
echo "Step 3: Testing connection from INSIDE the container to 127.0.0.1:"
docker exec dfs-lab04-broken curl -s http://127.0.0.1:8080 || docker exec dfs-lab04-broken python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8080').read().decode())"
echo "--> DIAGNOSIS: App works locally inside container, but host packets arriving on eth0 are rejected because socket is bound only to 127.0.0.1!"

echo ""
echo "Step 4: Starting container with server bound to 0.0.0.0..."
docker rm -f dfs-lab04-broken >/dev/null
docker run -d --name dfs-lab04-fixed -p 8080:8080 \
    -v "$CODE_DIR/server_fixed.py":/app.py \
    python:3.11-slim python3 /app.py >/dev/null
sleep 1

echo "Step 5: Testing connection from HOST after fix:"
curl -s http://localhost:8080
echo "--> SUCCESS: Socket bound to 0.0.0.0 accepts forwarded traffic from eth0!"

# Cleanup
docker rm -f dfs-lab04-fixed >/dev/null

echo ""
echo "Lab 04 Completed Successfully."
