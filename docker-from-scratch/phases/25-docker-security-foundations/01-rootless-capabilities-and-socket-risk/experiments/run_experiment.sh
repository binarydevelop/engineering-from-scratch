#!/usr/bin/env bash
# phases/25-docker-security-foundations/01-rootless-capabilities-and-socket-risk/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 25 Experiment: Docker Security Foundations ==="

echo "Step 1: Building hardened non-root container image"
docker build -t dfs-sec-hardened:v1 -f "$CODE_DIR/Dockerfile.hardened" "$CODE_DIR" >/dev/null

echo ""
echo "--- Experiment 1: The Default Insecurity (Running as Root UID 0) ---"
docker run --rm -v "$CODE_DIR/app.py":/app.py python:3.11-slim python3 /app.py

echo ""
echo "--- Experiment 2: Hardened Least Privilege (Running as UID 10001) ---"
docker run --rm dfs-sec-hardened:v1

echo ""
echo "--- Experiment 3: Read-Only Root Filesystem (--read-only) ---"
set +e
docker run --rm --read-only alpine:latest touch /etc/hacked.txt 2>&1
RO_EXIT=$?
set -e
echo "Exit Code with --read-only: $RO_EXIT (Read-only file system prevents tampering)"

echo ""
echo "--- Experiment 4: Dropping Linux Capabilities (--cap-drop ALL) ---"
echo "Attempting network interface configuration without CAP_NET_ADMIN:"
set +e
docker run --rm --cap-drop ALL alpine:latest ip link set lo down 2>&1
CAP_EXIT=$?
set -e
echo "Exit Code: $CAP_EXIT (Operation not permitted: kernel dropped capability!)"

echo ""
echo "--- Experiment 5: The Docker Socket Hazard ---"
echo "CONCEPTUAL LESSON: Mounting /var/run/docker.sock into a container gives that container"
echo "complete administrative control over the host Docker daemon. An attacker inside the container"
echo "can instruct the daemon to launch a container with '-v /:/host --privileged', immediately"
echo "escaping to the host operating system with root access! NEVER mount docker.sock into"
echo "untrusted application containers."

echo ""
echo "Phase 25 Experiment Completed Successfully."
