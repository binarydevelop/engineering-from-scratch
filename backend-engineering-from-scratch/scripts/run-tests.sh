#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="python3"
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

echo "Running complete test suite with $PYTHON_BIN..."
exec $PYTHON_BIN -m pytest -v "$@"
