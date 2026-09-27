#!/usr/bin/env bash
# phases/00-environment-and-orientation/01-verify-engine-and-client/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 00 Experiment ==="

echo "Step 1: Inspecting Docker CLI vs Engine via CLI"
docker version

echo ""
echo "Step 2: Proving Docker CLI is an HTTP client using raw Python socket script"
python3 "$LESSON_DIR/code/inspect_socket.py"

echo ""
echo "Step 3: Breaking the socket path to observe daemon unreachable error"
DOCKER_HOST="unix:///var/run/nonexistent_docker.sock" docker version 2>&1 || {
    echo "Observed expected failure: Docker CLI cannot function without the daemon socket."
}

echo ""
echo "Phase 00 Experiment Completed Successfully."
