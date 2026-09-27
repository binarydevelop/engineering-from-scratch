#!/usr/bin/env bash
# phases/28-container-debugging-without-magic/lab-02-immediate-exit/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 28 Lab 02: Immediate Exit ==="

# Cleanup prior containers
docker rm -f dfs-lab02-broken dfs-lab02-fixed >/dev/null 2>&1 || true

echo "Step 1: Building and running BROKEN image..."
docker build -q -f "$CODE_DIR/Dockerfile.broken" -t dfs-lab02:broken "$CODE_DIR" >/dev/null

set +e
docker run -d --name dfs-lab02-broken dfs-lab02:broken >/dev/null
RUN_EXIT=$?
sleep 1
set -e

echo ""
echo "Step 2: Checking container status (docker ps vs docker ps -a):"
echo "docker ps:"
docker ps --filter name=dfs-lab02-broken
echo "docker ps -a:"
docker ps -a --filter name=dfs-lab02-broken

EXIT_CODE=$(docker inspect dfs-lab02-broken --format '{{.State.ExitCode}}')
echo "--> DIAGNOSIS: Container exited immediately with exit code: $EXIT_CODE (127 = Executable not found in container rootfs!)"

echo ""
echo "Step 3: Building and running FIXED image..."
docker build -q -f "$CODE_DIR/Dockerfile.fixed" -t dfs-lab02:fixed "$CODE_DIR" >/dev/null
docker run --name dfs-lab02-fixed dfs-lab02:fixed

# Cleanup
docker rm -f dfs-lab02-broken dfs-lab02-fixed >/dev/null
docker rmi -f dfs-lab02:broken dfs-lab02:fixed >/dev/null 2>&1 || true

echo ""
echo "Lab 02 Completed Successfully."
