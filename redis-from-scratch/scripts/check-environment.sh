#!/usr/bin/env bash
# ==============================================================================
# check-environment.sh — Verify prerequisites for redis-from-scratch
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${BOLD}================================================================${RESET}"
echo -e "${BOLD}       redis-from-scratch — Environment Preflight Check         ${RESET}"
echo -e "${BOLD}================================================================${RESET}"

ERRORS=0
WARNINGS=0

check_cmd() {
    local cmd="$1"
    local desc="$2"
    local required="$3"
    
    if command -v "$cmd" >/dev/null 2>&1; then
        local version
        version=$("$cmd" --version 2>&1 | head -n 1 || true)
        echo -e "  [${GREEN}OK${RESET}] $desc: ${GREEN}$cmd${RESET} ($version)"
    else
        if [ "$required" = "true" ]; then
            echo -e "  [${RED}FAIL${RESET}] $desc: ${RED}$cmd not found${RESET} (Required)"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "  [${YELLOW}WARN${RESET}] $desc: ${YELLOW}$cmd not found${RESET} (Optional fallback available)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

echo -e "\n${BOLD}1. Core Runtimes & Interpreters:${RESET}"
check_cmd "python3" "Python 3 Interpreter" "true"

echo -e "\n${BOLD}2. Redis Tooling (Host vs Container):${RESET}"
check_cmd "redis-cli" "Redis CLI Client" "false"
check_cmd "redis-server" "Redis Server Engine (Host)" "false"
check_cmd "docker" "Docker Engine (Alternative runner)" "false"

echo -e "\n${BOLD}3. Networking Utilities:${RESET}"
check_cmd "nc" "Netcat (Raw socket inspection)" "false"
check_cmd "curl" "Curl utility" "false"

echo -e "\n${BOLD}4. Port 6379 Availability:${RESET}"
if command -v lsof >/dev/null 2>&1; then
    OCCUPIED=$(lsof -i :6379 -sTCP:LISTEN -t 2>/dev/null || true)
    if [ -n "$OCCUPIED" ]; then
        PROC=$(ps -p "$OCCUPIED" -o comm= 2>/dev/null || echo "Unknown")
        echo -e "  [${YELLOW}NOTE${RESET}] Port 6379 is currently active (PID: $OCCUPIED, Process: $PROC)"
        echo -e "         A Redis server is already listening on port 6379."
    else
        echo -e "  [${GREEN}OK${RESET}] Port 6379 is free and ready for experiments."
    fi
else
    echo -e "  [${YELLOW}INFO${RESET}] lsof command unavailable; skipping port scan."
fi

echo -e "\n${BOLD}----------------------------------------------------------------${RESET}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Preflight complete: Environment is ready for redis-from-scratch.${RESET}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}Note: Some optional utilities were not found. You can run either host Redis or Docker.${RESET}"
    fi
    exit 0
else
    echo -e "${RED}${BOLD}✗ Preflight failed: $ERRORS required dependencies missing.${RESET}"
    exit 1
fi
