#!/usr/bin/env bash
# phases/02-your-first-container/01-hello-world-dissected/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 02 Experiment: hello-world Dissected ==="

# Clean up prior test if exists
docker rm -f dfs-hello >/dev/null 2>&1 || true

echo "Step 1: Running docker run --name dfs-hello hello-world"
docker run --name dfs-hello hello-world

echo ""
echo "Step 2: Checking currently RUNNING containers (docker ps)"
docker ps --filter "name=dfs-hello"
echo "(Notice: The table is empty! Why?)"

echo ""
echo "Step 3: Checking ALL containers including stopped ones (docker ps -a)"
docker ps -a --filter "name=dfs-hello"

echo ""
echo "Step 4: Inspecting lifecycle state using Python script"
python3 "$LESSON_DIR/code/inspect_container_lifecycle.py" dfs-hello

echo ""
echo "Step 5: Cleaning up container"
docker rm dfs-hello

echo ""
echo "Phase 02 Experiment Completed Successfully."
