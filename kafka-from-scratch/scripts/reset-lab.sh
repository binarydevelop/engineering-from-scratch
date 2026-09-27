#!/usr/bin/env bash
# ==============================================================================
# reset-lab.sh — Completely wipe lab state, volumes, logs, and reset environment
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RESET="\033[0m"

cd "$(dirname "$0")/.."

echo -e "${YELLOW}${BOLD}Resetting Kafka Laboratory...${RESET}"

# Stop containers and tear down volumes
docker compose -f docker-compose.yml down -v --remove-orphans 2>/dev/null || true
docker compose -f docker-compose.cluster.yml down -v --remove-orphans 2>/dev/null || true

# Clean up any host temp logs or scratch data
rm -rf /tmp/kraft-combined-logs /tmp/kafka-lab-* outputs/*.log outputs/*.bin 2>/dev/null || true

echo -e "${GREEN}${BOLD}Reset complete.${RESET} All topics, partition logs, offset metadata, and volumes have been wiped clean."
echo -e "You can now run 'make up' or 'make up-cluster' for a pristine environment."
