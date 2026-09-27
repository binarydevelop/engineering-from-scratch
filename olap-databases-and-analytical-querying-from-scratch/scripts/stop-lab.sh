#!/usr/bin/env bash
set -euo pipefail

BOLD="\033[1m"
YELLOW="\033[0;33m"
GREEN="\033[0;32m"
RESET="\033[0m"

echo -e "${BOLD}${YELLOW}Stopping OLAP Database Lab Containers...${RESET}"
docker compose down

echo -e "${BOLD}${GREEN}[✓] All containerized OLAP lab services stopped successfully.${RESET}"
