#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================================="
echo " System Design From Scratch: Environment Checker"
echo "=========================================================="
echo ""

PASS=true

echo "1. Checking Core Toolchain:"
for tool in python3 curl git make; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "  [OK] $tool: $(command -v "$tool")"
    else
        echo "  [FAIL] $tool is missing!"
        PASS=false
    fi
done

echo ""
echo "2. Checking Python Environment:"
VENV_PYTHON="${REPO_ROOT}/.venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    echo "  [OK] Virtualenv detected at ${REPO_ROOT}/.venv"
    PY_VER=$("$VENV_PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
    echo "  [OK] Python version: $PY_VER"
else
    echo "  [WARN] Virtualenv not found. Run 'make setup'."
fi

echo ""
echo "3. Checking Simulation & Framework Libraries:"
for pkg in pytest httpx anyio fastapi uvicorn pydantic cryptography jwt; do
    if "$VENV_PYTHON" -c "import $pkg" >/dev/null 2>&1; then
        echo "  [OK] $pkg is available"
    else
        echo "  [FAIL] $pkg is NOT installed!"
        PASS=false
    fi
done

echo ""
echo "4. Testing Mathematical & Simulation Primitives:"
"$VENV_PYTHON" -c '
import math, hashlib, time
h = hashlib.sha256(b"system-design-test").hexdigest()
assert len(h) == 64
' && echo "  [OK] Standard cryptographic & mathematical hashing functional."

echo ""
echo "=========================================================="
if [ "$PASS" = true ]; then
    echo " RESULT: All critical toolchains verified! Ready to design."
    echo " Execute 'make test' to run all verification test suites."
else
    echo " RESULT: Some checks failed. Review output above."
    exit 1
fi
echo "=========================================================="
