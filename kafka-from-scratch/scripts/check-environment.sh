#!/usr/bin/env bash
# ==============================================================================
# check-environment.sh — Preflight verification for kafka-from-scratch
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${BOLD}================================================================${RESET}"
echo -e "${BOLD}       kafka-from-scratch — Environment Preflight Check         ${RESET}"
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
            echo -e "  [${YELLOW}WARN${RESET}] $desc: ${YELLOW}$cmd not found${RESET} (Optional)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

echo -e "\n${BOLD}1. Host Interpreters and Containers:${RESET}"
check_cmd "python3" "Python 3 Interpreter" "true"
check_cmd "docker" "Docker Engine" "true"

if command -v docker >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
        COMPOSE_VER=$(docker compose version 2>&1 | head -n 1)
        echo -e "  [${GREEN}OK${RESET}] Docker Compose: ${GREEN}docker compose${RESET} ($COMPOSE_VER)"
    else
        echo -e "  [${RED}FAIL${RESET}] Docker Compose v2 plugin is missing."
        ERRORS=$((ERRORS + 1))
    fi
fi

echo -e "\n${BOLD}2. Python Virtual Environment and Packages:${RESET}"
VENV_PYTHON="./.venv/bin/python3"
if [ -f "$VENV_PYTHON" ]; then
    echo -e "  [${GREEN}OK${RESET}] Dedicated virtual environment found at ./.venv"
    if $VENV_PYTHON -c "import confluent_kafka, kafka; print('Clients ready')" >/dev/null 2>&1; then
        echo -e "  [${GREEN}OK${RESET}] Python Kafka clients (confluent-kafka, kafka-python-ng): ${GREEN}Installed${RESET}"
    else
        echo -e "  [${YELLOW}WARN${RESET}] Python clients not fully installed in ./.venv. Run: pip install -r requirements.txt"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "  [${YELLOW}WARN${RESET}] No ./.venv detected. Create one with: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    WARNINGS=$((WARNINGS + 1))
fi

echo -e "\n${BOLD}3. Port Availability Checks:${RESET}"
check_port() {
    local port="$1"
    local desc="$2"
    if command -v lsof >/dev/null 2>&1; then
        OCCUPIED=$(lsof -i ":$port" -sTCP:LISTEN -t 2>/dev/null || true)
        if [ -n "$OCCUPIED" ]; then
            PROC=$(ps -p "$OCCUPIED" -o comm= 2>/dev/null || echo "Unknown")
            echo -e "  [${YELLOW}BUSY${RESET}] Port $port ($desc) is occupied by PID $OCCUPIED ($PROC)"
        else
            echo -e "  [${GREEN}OPEN${RESET}] Port $port ($desc) is available."
        fi
    elif command -v nc >/dev/null 2>&1; then
        if nc -z 127.0.0.1 "$port" 2>/dev/null; then
            echo -e "  [${YELLOW}BUSY${RESET}] Port $port ($desc) is currently in use."
        else
            echo -e "  [${GREEN}OPEN${RESET}] Port $port ($desc) is available."
        fi
    fi
}

check_port 9092 "Kafka Broker 1 (Single/Cluster)"
check_port 9094 "Kafka Broker 2 (Cluster)"
check_port 9096 "Kafka Broker 3 (Cluster)"

echo -e "\n${BOLD}4. Docker Image Verification:${RESET}"
if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "apache/kafka:3.8.0"; then
    echo -e "  [${GREEN}OK${RESET}] Local Docker image cache has ${GREEN}apache/kafka:3.8.0${RESET}"
else
    echo -e "  [${YELLOW}INFO${RESET}] apache/kafka:3.8.0 not yet downloaded. Will pull on first run."
fi

echo -e "\n${BOLD}----------------------------------------------------------------${RESET}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}${BOLD}Preflight check passed successfully!${RESET} Ready to learn."
    exit 0
else
    echo -e "${RED}${BOLD}Preflight check failed with $ERRORS fatal error(s).${RESET}"
    exit 1
fi
