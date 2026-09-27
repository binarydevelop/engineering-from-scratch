#!/usr/bin/env bash
# phases/24-debugging-containers/01-systematic-container-diagnostics/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 24 Experiment: Systematic Diagnostics ==="

# Cleanup prior containers
docker rm -f dfs-diag-broken dfs-diag-oom >/dev/null 2>&1 || true

echo "Case 1: Diagnosing an immediately exited container with error code 2..."
docker run -d --name dfs-diag-broken alpine:latest sh -c "echo 'FATAL: Configuration key DATABASE_URL is required but missing' >&2; exit 2" >/dev/null
sleep 1

bash "$CODE_DIR/diagnose.sh" dfs-diag-broken

echo ""
echo "Case 2: Diagnosing an OOM killed container..."
set +e
docker run -d --name dfs-diag-oom -m 30m --memory-swap 30m python:3.11-slim python3 -c "b = b'X' * (50*1024*1024)" >/dev/null
sleep 1
set -e

bash "$CODE_DIR/diagnose.sh" dfs-diag-oom

# Cleanup
docker rm -f dfs-diag-broken dfs-diag-oom >/dev/null

echo ""
echo "Phase 24 Experiment Completed Successfully."
