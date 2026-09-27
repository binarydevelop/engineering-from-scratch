#!/usr/bin/env bash
# ==============================================================================
# stop-kafka.sh — Stop running Kafka containers
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
RESET="\033[0m"

cd "$(dirname "$0")/.."

echo -e "${BOLD}Stopping single-broker lab...${RESET}"
docker compose -f docker-compose.yml down --remove-orphans 2>/dev/null || true

echo -e "${BOLD}Stopping 3-node cluster lab...${RESET}"
docker compose -f docker-compose.cluster.yml down --remove-orphans 2>/dev/null || true

echo -e "${GREEN}All Kafka lab containers have been stopped.${RESET}"
