#!/usr/bin/env bash
# phases/17-signals-pid1-and-lifecycle/01-sigterm-propagation-and-pid1/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 17 Experiment: Signals, PID 1, and Shutdown ==="

# Cleanup prior containers
docker rm -f dfs-exec-demo dfs-shell-demo >/dev/null 2>&1 || true

echo "Building images..."
docker build -q -f "$CODE_DIR/Dockerfile.exec" -t dfs-sig-exec:v1 "$CODE_DIR" >/dev/null
docker build -q -f "$CODE_DIR/Dockerfile.shell" -t dfs-sig-shell:v1 "$CODE_DIR" >/dev/null

echo ""
echo "--- Test 1: The Correct Approach (Exec Form: CMD [\"python3\", ...]) ---"
docker run -d --name dfs-exec-demo dfs-sig-exec:v1 >/dev/null
sleep 1

echo "Stopping dfs-exec-demo with 'docker stop' (timing shutdown)..."
START_TIME=$(date +%s)
docker stop dfs-exec-demo >/dev/null
DURATION=$(( $(date +%s) - START_TIME ))
echo "Exec form container stopped gracefully in: ${DURATION}s"

echo "Container logs during shutdown:"
docker logs dfs-exec-demo
docker rm -f dfs-exec-demo >/dev/null

echo ""
echo "--- Test 2: The Broken Shell Form (CMD python3 ...) ---"
docker run -d --name dfs-shell-demo dfs-sig-shell:v1 >/dev/null
sleep 1

echo "Stopping dfs-shell-demo with 'docker stop' (Watch the 10-second SIGKILL hang)..."
START_TIME=$(date +%s)
docker stop -t 3 dfs-shell-demo >/dev/null  # Using -t 3 to avoid waiting full 10s while still demonstrating grace period timeout
DURATION=$(( $(date +%s) - START_TIME ))
echo "Shell form container took ${DURATION}s to exit (SIGTERM was ignored; killed by SIGKILL!)"

EXIT_CODE=$(docker inspect dfs-shell-demo --format '{{.State.ExitCode}}')
echo "Exit Code: $EXIT_CODE (Notice: 137 = forced SIGKILL termination)"

docker rm -f dfs-shell-demo >/dev/null

echo ""
echo "Phase 17 Experiment Completed Successfully."
