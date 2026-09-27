#!/usr/bin/env bash
# phases/12-volumes-and-persistence/01-named-volumes-lifecycle/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 12 Experiment: Volumes and Persistence ==="

# Cleanup prior test resources
docker rm -f dfs-ephemeral-1 dfs-ephemeral-2 dfs-vol-c1 dfs-vol-c2 >/dev/null 2>&1 || true
docker volume rm dfs-data-vol >/dev/null 2>&1 || true

echo "--- Part 1: The Ephemeral Layer Trap (Data Loss) ---"
echo "1. Writing state to ephemeral container rootfs..."
docker run --name dfs-ephemeral-1 -v "$CODE_DIR/state_recorder.py":/state_recorder.py \
    python:3.11-slim python3 /state_recorder.py write "Ephemeral Transaction 1"

echo "2. Deleting the container (docker rm -f dfs-ephemeral-1)..."
docker rm -f dfs-ephemeral-1 >/dev/null

echo "3. Starting brand new container from same image and reading state (Expect Failure):"
set +e
docker run --name dfs-ephemeral-2 -v "$CODE_DIR/state_recorder.py":/state_recorder.py \
    python:3.11-slim python3 /state_recorder.py read
READ_EXIT=$?
set -e
docker rm -f dfs-ephemeral-2 >/dev/null

if [ "$READ_EXIT" -ne 0 ]; then
    echo "--> OBSERVED: Data was completely lost when container was deleted!"
fi

echo ""
echo "--- Part 2: The Named Volume Solution (Persistent Lifecycle) ---"
echo "1. Creating Docker named volume: dfs-data-vol"
docker volume create dfs-data-vol

echo "2. Inspecting volume metadata (Mountpoint on Docker host/VM):"
docker volume inspect dfs-data-vol --format 'Mountpoint: {{.Mountpoint}}'

echo ""
echo "3. Launching dfs-vol-c1 mounting -v dfs-data-vol:/data and writing records..."
docker run --name dfs-vol-c1 \
    -v dfs-data-vol:/data \
    -v "$CODE_DIR/state_recorder.py":/state_recorder.py \
    python:3.11-slim python3 /state_recorder.py write "Persistent Record #101"

docker run --rm \
    -v dfs-data-vol:/data \
    -v "$CODE_DIR/state_recorder.py":/state_recorder.py \
    python:3.11-slim python3 /state_recorder.py write "Persistent Record #102"

echo ""
echo "4. Completely destroying container dfs-vol-c1..."
docker rm -f dfs-vol-c1 >/dev/null

echo ""
echo "5. Launching completely new container dfs-vol-c2 attached to same volume:"
docker run --name dfs-vol-c2 \
    -v dfs-data-vol:/data \
    -v "$CODE_DIR/state_recorder.py":/state_recorder.py \
    python:3.11-slim python3 /state_recorder.py read

echo "--> VERIFIED: State survived container destruction!"

# Cleanup
docker rm -f dfs-vol-c2 >/dev/null
docker volume rm dfs-data-vol >/dev/null

echo ""
echo "Phase 12 Experiment Completed Successfully."
