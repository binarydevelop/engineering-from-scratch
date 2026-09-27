#!/usr/bin/env bash
set -euo pipefail

# scripts/check-environment.sh
# Verifies that host prerequisites and tools meet the course standards.

echo "=========================================================="
echo "    kubernetes-from-scratch: Environment Verification     "
echo "=========================================================="

FAILED=0

check_cmd() {
    local cmd="$1"
    local desc="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        local version=""
        if [ "$cmd" = "kubectl" ]; then
            version=$(kubectl version --client 2>&1 | head -n 1 || true)
        elif [ "$cmd" = "helm" ]; then
            version=$(helm version 2>&1 | head -n 1 || true)
        else
            version=$("$cmd" --version 2>&1 | head -n 1 || true)
        fi
        echo "  [OK] $cmd ($desc): $version"
    else
        echo "  [FAIL] $cmd ($desc) is NOT installed or not on PATH."
        FAILED=1
    fi
}

echo ""
echo "1. Checking CLI Tooling..."
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

check_cmd docker "Container Engine"
check_cmd kind "Local Multi-Node Kubernetes"
check_cmd kubectl "Kubernetes CLI API Client"
check_cmd python3 "Python 3 Interpreter"
check_cmd helm "Kubernetes Package Manager"

echo ""
echo "2. Checking Docker Daemon Status..."
if docker info >/dev/null 2>&1; then
    SERVER_OS=$(docker info --format '{{.OperatingSystem}}')
    CPUS=$(docker info --format '{{.NCPU}}')
    MEM_BYTES=$(docker info --format '{{.MemTotal}}')
    MEM_GB=$(( MEM_BYTES / 1024 / 1024 / 1024 ))
    echo "  [OK] Docker Daemon is responsive."
    echo "       Host/VM OS : $SERVER_OS"
    echo "       CPUs       : $CPUS cores"
    echo "       Memory     : ${MEM_GB} GB"

    if [ "$MEM_GB" -lt 4 ]; then
        echo "  [WARN] Docker memory is less than 4GB. Multi-node labs may face memory pressure."
    fi
else
    echo "  [FAIL] Docker daemon is not running or socket is inaccessible."
    FAILED=1
fi

echo ""
echo "3. Checking Python Version Compatibility..."
if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
        echo "  [OK] Python version $PY_VER meets requirement (>= 3.10)."
    else
        echo "  [FAIL] Python version $PY_VER is too old. Please install Python >= 3.10."
        FAILED=1
    fi
fi

echo ""
echo "=========================================================="
if [ "$FAILED" -eq 0 ]; then
    echo "  RESULT: Environment meets all prerequisites!"
    echo "  You are ready to run: make cluster-up"
else
    echo "  RESULT: Prerequisites missing. Please install missing tools."
    exit 1
fi
echo "=========================================================="
