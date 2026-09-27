#!/usr/bin/env bash
# ==============================================================================
# stop-redis.sh — Stop Redis standalone laboratory
# ==============================================================================

set -euo pipefail

PORT="${1:-6379}"

echo "Stopping Redis Laboratory on Port $PORT..."

# Try graceful redis-cli SHUTDOWN first
if command -v redis-cli >/dev/null 2>&1; then
    redis-cli -p "$PORT" SHUTDOWN NOSAVE 2>/dev/null || true
fi

# Stop docker container if running
if command -v docker >/dev/null 2>&1; then
    docker stop redis-scratch-lab 2>/dev/null || true
    docker stop redis-primary 2>/dev/null || true
fi

# Kill remaining local process if still bound
if command -v lsof >/dev/null 2>&1; then
    PID=$(lsof -i :"$PORT" -sTCP:LISTEN -t 2>/dev/null || true)
    if [ -n "$PID" ]; then
        kill "$PID" 2>/dev/null || true
        echo "Terminated PID $PID on port $PORT"
    fi
fi

echo "Redis stopped."
