#!/usr/bin/env bash
# ==============================================================================
# start-redis.sh — Start Redis standalone laboratory
# ==============================================================================

set -euo pipefail

MODE="${1:-auto}"
PORT="${2:-6379}"

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${BOLD}Starting Redis Laboratory on Port $PORT (Mode: $MODE)...${RESET}"

# Check if port is already listening
if command -v lsof >/dev/null 2>&1; then
    if lsof -i :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${GREEN}A service is already listening on port $PORT.${RESET}"
        if command -v redis-cli >/dev/null 2>&1; then
            if redis-cli -p "$PORT" PING 2>/dev/null | grep -q "PONG"; then
                echo -e "${GREEN}Confirmed: Redis is responsive (PING -> PONG). Ready to proceed!${RESET}"
                exit 0
            fi
        fi
    fi
fi

if [ "$MODE" = "local" ] || { [ "$MODE" = "auto" ] && command -v redis-server >/dev/null 2>&1; }; then
    echo -e "${BOLD}Launching local host redis-server daemon on port $PORT...${RESET}"
    redis-server --daemonize yes --port "$PORT" --protected-mode no --loglevel notice --dir /tmp
    sleep 1
    if redis-cli -p "$PORT" PING | grep -q "PONG"; then
        echo -e "${GREEN}✓ Local redis-server started successfully on port $PORT.${RESET}"
        exit 0
    fi
fi

if [ "$MODE" = "docker" ] || { [ "$MODE" = "auto" ] && command -v docker >/dev/null 2>&1; }; then
    echo -e "${BOLD}Launching Redis via Docker container on port $PORT...${RESET}"
    docker run -d --name redis-scratch-lab -p "$PORT":6379 --rm redis:7-alpine redis-server --protected-mode no
    sleep 1
    if command -v redis-cli >/dev/null 2>&1; then
        redis-cli -p "$PORT" PING
    else
        docker exec redis-scratch-lab redis-cli PING
    fi
    echo -e "${GREEN}✓ Docker Redis container started successfully on port $PORT.${RESET}"
    exit 0
fi

echo "Error: Neither local redis-server nor docker was found to launch Redis."
exit 1
