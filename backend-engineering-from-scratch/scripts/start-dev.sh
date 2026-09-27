#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"
HOST="${HOST:-127.0.0.1}"
APP_MODULE="${1:-apps.01_modular_monolith.main:app}"

echo "Starting Backend Dev Server on http://${HOST}:${PORT}..."
echo "Target Module: ${APP_MODULE}"

PYTHON_BIN="python3"
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

exec $PYTHON_BIN -m uvicorn "${APP_MODULE}" --host "${HOST}" --port "${PORT}" --reload
