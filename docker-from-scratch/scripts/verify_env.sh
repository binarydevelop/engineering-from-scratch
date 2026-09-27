#!/usr/bin/env bash
# scripts/verify_env.sh
# Verifies the user's host environment and Docker engine connectivity.

set -euo pipefail

echo "============================================================"
echo "    DOCKER FROM SCRATCH: Environment Verification"
echo "============================================================"

FAILED=0

check_cmd() {
    local cmd="$1"
    local desc="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        echo " [OK] $desc: $(which "$cmd")"
    else
        echo " [FAIL] $desc ($cmd) is missing."
        FAILED=1
    fi
}

echo "--- 1. Basic CLI Utilities ---"
check_cmd python3 "Python 3 Interpreter"
check_cmd curl "cURL HTTP Client"
check_cmd git "Git Version Control"

echo ""
echo "--- 2. Docker CLI & Compose ---"
check_cmd docker "Docker CLI"
if docker compose version >/dev/null 2>&1; then
    echo " [OK] Docker Compose: $(docker compose version)"
else
    echo " [FAIL] Docker Compose plugin is missing or malfunctioning."
    FAILED=1
fi

echo ""
echo "--- 3. Docker Daemon Connectivity ---"
if docker info >/dev/null 2>&1; then
    echo " [OK] Docker Engine is active and responding."
    SERVER_OS=$(docker version --format '{{.Server.Os}}')
    SERVER_ARCH=$(docker version --format '{{.Server.Arch}}')
    CLIENT_OS=$(docker version --format '{{.Client.Os}}')
    CLIENT_ARCH=$(docker version --format '{{.Client.Arch}}')
    echo "      Client OS/Arch: ${CLIENT_OS}/${CLIENT_ARCH}"
    echo "      Server OS/Arch: ${SERVER_OS}/${SERVER_ARCH}"
    
    if [ "$CLIENT_OS" != "linux" ]; then
        echo "      [NOTE] Running Docker Desktop on ${CLIENT_OS}. Containers execute inside a lightweight Linux VM."
    else
        echo "      [NOTE] Running natively on Linux. Container namespaces map directly to host kernel."
    fi
else
    echo " [FAIL] Docker daemon is unreachable. Ensure Docker Desktop or Docker Engine is running."
    FAILED=1
fi

echo ""
echo "--- 4. Summary ---"
if [ "$FAILED" -eq 0 ]; then
    echo "All core requirements satisfied. You are ready to start Phase 00!"
    exit 0
else
    echo "Please resolve the above failures before proceeding."
    exit 1
fi
