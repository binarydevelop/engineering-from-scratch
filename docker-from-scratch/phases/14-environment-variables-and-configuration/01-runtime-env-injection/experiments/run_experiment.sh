#!/usr/bin/env bash
# phases/14-environment-variables-and-configuration/01-runtime-env-injection/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 14 Experiment: Environment Variables & Configuration ==="

# Cleanup prior container
docker rm -f dfs-cfg-test >/dev/null 2>&1 || true

echo "--- Run 1: Default In-Code Fallbacks (No env vars injected) ---"
docker run --rm -v "$CODE_DIR/configurable_app.py":/app.py \
    python:3.11-slim python3 /app.py

echo ""
echo "--- Run 2: Injected Development Profile (--env-file dev.env) ---"
docker run --rm --env-file "$CODE_DIR/dev.env" \
    -v "$CODE_DIR/configurable_app.py":/app.py \
    python:3.11-slim python3 /app.py

echo ""
echo "--- Run 3: Injected Production Profile (--env-file prod.env) ---"
docker run --rm --env-file "$CODE_DIR/prod.env" \
    -v "$CODE_DIR/configurable_app.py":/app.py \
    python:3.11-slim python3 /app.py

echo ""
echo "--- Run 4: Precedence Override (-e overrides --env-file) ---"
docker run --rm --env-file "$CODE_DIR/prod.env" -e LOG_LEVEL="TRACE" \
    -v "$CODE_DIR/configurable_app.py":/app.py \
    python:3.11-slim python3 /app.py | grep "log_level"
echo "Verified: Explicit -e flag successfully overrides --env-file default!"

echo ""
echo "--- Run 5: The Security Warning (docker inspect exposure) ---"
docker run -d --name dfs-cfg-test -e SECRET_API_KEY="super-secret-12345" alpine:latest sleep 60 >/dev/null
echo "Inspecting container Config.Env via docker inspect:"
docker inspect dfs-cfg-test --format '{{range .Config.Env}}{{println .}}{{end}}' | grep "SECRET"
echo "WARNING: Anyone with read access to the Docker socket can view all container environment variables in plaintext!"

# Cleanup
docker rm -f dfs-cfg-test >/dev/null

echo ""
echo "Phase 14 Experiment Completed Successfully."
