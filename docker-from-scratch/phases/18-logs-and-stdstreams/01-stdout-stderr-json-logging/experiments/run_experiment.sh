#!/usr/bin/env bash
# phases/18-logs-and-stdstreams/01-stdout-stderr-json-logging/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 18 Experiment: Logs & stdstreams ==="

# Cleanup prior container
docker rm -f dfs-logger >/dev/null 2>&1 || true

echo "Step 1: Running container that emits to stdout and stderr"
docker run --name dfs-logger \
    -v "$CODE_DIR/logger_app.py":/app.py \
    python:3.11-slim python3 /app.py

echo ""
echo "Step 2: Inspecting container logs using 'docker logs'"
docker logs dfs-logger

echo ""
echo "Step 3: Separating stdout from stderr via stream redirection"
mkdir -p /tmp/dfs_logs
docker logs dfs-logger > /tmp/dfs_logs/stdout.txt 2> /tmp/dfs_logs/stderr.txt

echo "Captured stdout stream:"
cat /tmp/dfs_logs/stdout.txt
echo ""
echo "Captured stderr stream:"
cat /tmp/dfs_logs/stderr.txt

echo ""
echo "Step 4: Inspecting Docker's logging driver metadata"
LOG_PATH=$(docker inspect dfs-logger --format '{{.LogPath}}')
echo "Container Log Path in Engine: $LOG_PATH"
echo "Logging Driver: $(docker inspect dfs-logger --format '{{.HostConfig.LogConfig.Type}}')"

# Cleanup
rm -rf /tmp/dfs_logs
docker rm -f dfs-logger >/dev/null

echo ""
echo "Phase 18 Experiment Completed Successfully."
