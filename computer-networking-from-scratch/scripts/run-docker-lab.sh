#!/usr/bin/env bash
# ==============================================================================
# run-docker-lab.sh
# Runs Linux network namespace labs inside a privileged Docker container
# (Enables macOS and Windows users to run native Linux networking experiments)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: Docker is not installed or not in PATH."
    exit 1
fi

echo "==> Building / launching isolated Linux network lab container..."

docker run --rm -it \
    --privileged \
    --name net-lab \
    -v "${REPO_DIR}:/workspace" \
    -w /workspace \
    debian:12-slim \
    bash -c '
        echo "Installing Linux networking utilities inside container...";
        apt-get update -qq && apt-get install -qq -y \
            iproute2 iptables nftables tcpdump curl netcat-traditional \
            procps python3 python3-pip make gcc >/dev/null 2>&1;
        echo "==================================================================";
        echo "Container environment ready with full Linux networking stack!";
        echo "You can now run:";
        echo "  ./scripts/create-network-lab.sh";
        echo "  make test";
        echo "==================================================================";
        exec bash
    '
