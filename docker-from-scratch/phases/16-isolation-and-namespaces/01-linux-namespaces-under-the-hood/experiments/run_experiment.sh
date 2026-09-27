#!/usr/bin/env bash
# phases/16-isolation-and-namespaces/01-linux-namespaces-under-the-hood/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 16 Experiment: Isolation and Namespaces ==="

# Cleanup prior container
docker rm -f dfs-ns-demo >/dev/null 2>&1 || true

echo "Step 1: Launching container with custom UTS hostname and isolated sleep process"
docker run -d --name dfs-ns-demo --hostname isolated-box-01 alpine:latest sleep 120 >/dev/null

echo ""
echo "Step 2: Proving UTS (Hostname) Namespace Isolation"
HOST_HOSTNAME=$(hostname)
CONTAINER_HOSTNAME=$(docker exec dfs-ns-demo hostname)
echo "Host Machine Hostname:      $HOST_HOSTNAME"
echo "Inside Container Hostname:  $CONTAINER_HOSTNAME"

echo ""
echo "Step 3: Proving PID Namespace Dual-Identity (Inside vs Outside)"
python3 "$LESSON_DIR/code/inspect_namespaces.py" dfs-ns-demo

echo ""
echo "Step 4: Proving Mount Namespace Isolation"
echo "Container root directory:"
docker exec dfs-ns-demo sh -c "ls -d /* | head -n 5"

# Cleanup
docker rm -f dfs-ns-demo >/dev/null

echo ""
echo "Phase 16 Experiment Completed Successfully."
