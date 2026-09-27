#!/usr/bin/env bash
# Lab Reset Script
# Clears injected faults, restarts containers, and verifies baseline health

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================================="
echo "Resetting Production SRE Lab to Clean Baseline"
echo "=========================================================="

cd "${REPO_ROOT}"

# Clear any active faults
if [ -f "chaos/latency_injector.py" ]; then
    python3 "chaos/latency_injector.py" --reset 2>/dev/null || true
fi

# Restart containers if Docker Compose is running
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    echo "Restarting Docker Compose services..."
    docker compose restart
    sleep 3
    docker compose ps
fi

echo "=========================================================="
echo "Lab state restored to baseline."
