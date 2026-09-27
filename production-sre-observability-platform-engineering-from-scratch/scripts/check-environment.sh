#!/usr/bin/env bash
# Environment Verification Script
# Verifies host dependencies: Python, Docker, Docker Compose, Curl, Git

set -euo pipefail

echo "=========================================================="
echo "Production SRE Lab: Checking Host Environment Pre-Flight"
echo "=========================================================="

FAILED=0

# Check Python 3.11+
if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 11 ]; then
        echo " [OK] Python version: $PY_VER (>= 3.11 requirement met)"
    else
        echo " [FAIL] Python version: $PY_VER. Python 3.11 or higher is required."
        FAILED=1
    fi
else
    echo " [FAIL] python3 not found on PATH."
    FAILED=1
fi

# Check Docker
if command -v docker >/dev/null 2>&1; then
    DOCKER_VER=$(docker --version | awk '{print $3}' | tr -d ',')
    echo " [OK] Docker version: $DOCKER_VER"
else
    echo " [WARN] docker binary not found on PATH. Docker is required for Tier 1 container labs."
fi

# Check Docker Compose
if docker compose version >/dev/null 2>&1; then
    COMPOSE_VER=$(docker compose version --short 2>/dev/null || echo "detected")
    echo " [OK] Docker Compose v2: $COMPOSE_VER"
else
    echo " [WARN] docker compose v2 plugin not detected. Local container labs require compose v2."
fi

# Check Curl
if command -v curl >/dev/null 2>&1; then
    CURL_VER=$(curl --version | head -n 1 | awk '{print $2}')
    echo " [OK] Curl version: $CURL_VER"
else
    echo " [FAIL] curl binary not found on PATH."
    FAILED=1
fi

# Check Git
if command -v git >/dev/null 2>&1; then
    GIT_VER=$(git --version | awk '{print $3}')
    echo " [OK] Git version: $GIT_VER"
else
    echo " [FAIL] git not found on PATH."
    FAILED=1
fi

echo "=========================================================="
if [ "$FAILED" -eq 0 ]; then
    echo "Pre-flight checks passed! Your host environment is ready."
    exit 0
else
    echo "Pre-flight checks failed. Please install missing dependencies."
    exit 1
fi
