#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " Backend Engineering From Scratch: Environment Checker"
echo "=========================================================="

ERRORS=0
WARNINGS=0

check_cmd() {
    local cmd="$1"
    local desc="$2"
    local required="${3:-true}"
    if command -v "$cmd" >/dev/null 2>&1; then
        local version
        version=$("$cmd" --version 2>&1 | head -n 1 || echo "installed")
        echo "  [OK] $desc ($cmd): $version"
    else
        if [ "$required" = "true" ]; then
            echo "  [FAIL] $desc ($cmd) is REQUIRED but not found in PATH."
            ERRORS=$((ERRORS + 1))
        else
            echo "  [WARN] $desc ($cmd) is optional (used for extended container/remote labs)."
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

echo ""
echo "1. Checking Core Toolchain:"
check_cmd "python3" "Python Runtime" "true"
check_cmd "curl" "HTTP Client" "true"
check_cmd "git" "Version Control" "true"
check_cmd "docker" "Container Engine" "false"

echo ""
echo "2. Checking Python Environment:"
PYTHON_BIN="python3"
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
    echo "  [OK] Virtual environment found at .venv"
else
    echo "  [WARN] .venv not found. Run 'make setup' to initialize."
    WARNINGS=$((WARNINGS + 1))
fi

PY_VER=$($PYTHON_BIN -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
PY_MAJOR=$($PYTHON_BIN -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON_BIN -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 12 ]; then
    echo "  [OK] Python version is $PY_VER (>= 3.12 required)"
else
    echo "  [FAIL] Python version is $PY_VER. Python 3.12+ is required."
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "3. Checking Python Standard Modules (Zero-Dependency Baselines):"
$PYTHON_BIN -c "import socket, http.server, urllib.request, asyncio, sqlite3, hashlib, hmac, secrets, multiprocessing, threading; print('  [OK] Standard library socket, http.server, sqlite3, asyncio, crypto modules verified.')"

echo ""
echo "4. Checking Framework & Validation Packages:"
check_package() {
    local pkg="$1"
    if $PYTHON_BIN -c "import $pkg" >/dev/null 2>&1; then
        local ver
        ver=$($PYTHON_BIN -c "import $pkg; print(getattr($pkg, '__version__', 'available'))")
        echo "  [OK] $pkg: $ver"
    else
        echo "  [FAIL] Python package '$pkg' is missing. Run 'uv pip install -r requirements.txt'."
        ERRORS=$((ERRORS + 1))
    fi
}

check_package "fastapi"
check_package "pydantic"
check_package "uvicorn"
check_package "httpx"
check_package "pytest"
check_package "jwt"
check_package "bcrypt"

echo ""
echo "5. Verifying Socket Binding Capability:"
$PYTHON_BIN -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.listen(1)
    print(f'  [OK] Successfully bound and listened on loopback dynamic port {port}')
finally:
    s.close()
"

echo ""
echo "=========================================================="
if [ "$ERRORS" -eq 0 ]; then
    echo " RESULT: All critical requirements satisfied! Ready to learn."
    echo " Run 'make test' or proceed to 'phases/00-backend-engineering-lab'."
    exit 0
else
    echo " RESULT: Found $ERRORS errors and $WARNINGS warnings."
    echo " Please resolve errors before proceeding."
    exit 1
fi
