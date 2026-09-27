#!/usr/bin/env bash
# Lab Teardown Script
# Stops Tier 1 local containers gracefully

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Stopping Production SRE Lab environment..."

cd "${REPO_ROOT}"

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    docker compose down --remove-orphans
    echo "Containers stopped cleanly."
fi

# Clean up any lingering background local processes
pkill -f "uvicorn services." 2>/dev/null || true
pkill -f "python3.*services/" 2>/dev/null || true

echo "Lab shutdown complete."
