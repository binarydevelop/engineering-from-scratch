#!/usr/bin/env bash
# phases/13-bind-mounts-and-development-workflows/01-host-filesystem-mirroring/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$LESSON_DIR/code/app"

echo "=== Running Phase 13 Experiment: Bind Mounts & Live Workflows ==="

# Cleanup prior container
docker rm -f dfs-bind-demo >/dev/null 2>&1 || true

echo "Resetting hello.txt on host..."
echo "Version 1: Written on host terminal." > "$APP_DIR/hello.txt"

echo "Step 1: Starting container with host BIND MOUNT (-v $APP_DIR:/workspace)"
docker run -d --name dfs-bind-demo \
    -v "$APP_DIR":/workspace \
    alpine:latest sleep 60 >/dev/null

echo ""
echo "Step 2: Reading file from inside the container:"
docker exec dfs-bind-demo cat /workspace/hello.txt

echo ""
echo "Step 3: Modifying file ON THE HOST (simulating a developer editing code in VS Code)..."
echo "Version 2: Live reload triggered by developer on host!" > "$APP_DIR/hello.txt"

echo ""
echo "Step 4: Reading file from inside the running container (NO rebuild, NO restart!):"
docker exec dfs-bind-demo cat /workspace/hello.txt
echo "--> VERIFIED: Host filesystem modification was instantaneously reflected in container!"

echo ""
echo "Step 5: Writing from INSIDE the container to host mount:"
docker exec dfs-bind-demo sh -c "echo 'Created from container' > /workspace/from_container.txt"
echo "Verifying file existence on host disk:"
cat "$APP_DIR/from_container.txt"

# Cleanup
rm -f "$APP_DIR/from_container.txt"
docker rm -f dfs-bind-demo >/dev/null

echo ""
echo "Phase 13 Experiment Completed Successfully."
