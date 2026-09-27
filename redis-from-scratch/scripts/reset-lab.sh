#!/usr/bin/env bash
# ==============================================================================
# reset-lab.sh — Flush database keys and clear test persistence files
# ==============================================================================

set -euo pipefail

PORT="${1:-6379}"

BOLD="\033[1m"
GREEN="\033[0;32m"
RESET="\033[0m"

echo -e "${BOLD}Resetting Redis Lab on Port $PORT...${RESET}"

if command -v redis-cli >/dev/null 2>&1; then
    if redis-cli -p "$PORT" PING >/dev/null 2>&1; then
        redis-cli -p "$PORT" FLUSHALL SYNC
        KEY_COUNT=$(redis-cli -p "$PORT" DBSIZE)
        echo -e "${GREEN}✓ FLUSHALL executed. DBSIZE is now: $KEY_COUNT${RESET}"
    fi
elif command -v docker >/dev/null 2>&1; then
    if docker ps | grep -q "redis"; then
        CONTAINER=$(docker ps --filter "name=redis" --format "{{.ID}}" | head -n 1)
        docker exec "$CONTAINER" redis-cli FLUSHALL SYNC
        echo -e "${GREEN}✓ Docker Redis flushed.${RESET}"
    fi
fi

# Clean local working directory artifacts
rm -rf dump.rdb appendonly.aof appendonlydir/
echo -e "${GREEN}✓ Cleaned local persistence artifacts (RDB/AOF). Lab is reset.${RESET}"
