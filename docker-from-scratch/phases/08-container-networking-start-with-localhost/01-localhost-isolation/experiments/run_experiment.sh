#!/usr/bin/env bash
# phases/08-container-networking-start-with-localhost/01-localhost-isolation/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 08 Experiment: The Localhost Trap ==="

echo "Step 1: Starting server.py directly on the HOST machine (port 8080)..."
python3 "$LESSON_DIR/code/server.py" >/dev/null 2>&1 &
HOST_PID=$!
sleep 1

cleanup() {
    echo "Cleaning up host process PID $HOST_PID..."
    kill -TERM "$HOST_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "Step 2: Testing connection from HOST to HOST (curl localhost:8080)"
HOST_RESPONSE=$(curl -s http://localhost:8080)
echo "Success! Response from host terminal:"
echo "$HOST_RESPONSE"

echo ""
echo "Step 3: Testing connection from INSIDE A CONTAINER to localhost:8080"
echo "Command: docker run --rm alpine:latest wget -qO- --timeout=2 http://localhost:8080"
set +e
CONTAINER_OUTPUT=$(docker run --rm alpine:latest wget -qO- -T 2 http://localhost:8080 2>&1)
EXIT_CODE=$?
set -e

echo "Exit Code: $EXIT_CODE"
echo "Output: $CONTAINER_OUTPUT"
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "--> OBSERVED: Inside the container, 'localhost:8080' completely failed!"
    echo "--> REASON: 'localhost' inside the container resolves to the container's private loopback interface (lo)."
fi

echo ""
echo "Step 4: Connecting from container to host using 'host.docker.internal' (Desktop routing)"
set +e
DESKTOP_OUTPUT=$(docker run --rm --add-host=host.docker.internal:host-gateway alpine:latest wget -qO- -T 2 http://host.docker.internal:8080 2>&1)
DESKTOP_EXIT=$?
set -e
if [ "$DESKTOP_EXIT" -eq 0 ]; then
    echo "Success! Reached host via host.docker.internal:"
    echo "$DESKTOP_OUTPUT"
fi

echo ""
echo "Phase 08 Experiment Completed Successfully."
