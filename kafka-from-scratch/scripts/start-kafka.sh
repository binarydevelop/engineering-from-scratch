#!/usr/bin/env bash
# ==============================================================================
# start-kafka.sh — Launch Kafka Lab (Single broker or 3-node cluster)
# ==============================================================================

set -euo pipefail

MODE="${1:-single}"

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${BOLD}================================================================${RESET}"
echo -e "${BOLD}Starting Kafka Laboratory in mode: ${GREEN}${MODE}${RESET}"
echo -e "${BOLD}================================================================${RESET}"

cd "$(dirname "$0")/.."

if [ "$MODE" = "cluster" ]; then
    echo -e "Launching 3-node KRaft cluster via docker compose..."
    docker compose -f docker-compose.cluster.yml up -d
    echo -e "Waiting for KRaft quorum to unfence and become healthy..."
    
    for i in {1..30}; do
        if docker compose -f docker-compose.cluster.yml ps | grep -q "healthy"; then
            echo -e "${GREEN}3-node Kafka cluster is running and healthy!${RESET}"
            echo -e "Brokers available at: localhost:9092, localhost:9094, localhost:9096"
            exit 0
        fi
        sleep 1
    done
    echo -e "${YELLOW}Cluster is starting up; check logs with: make logs-cluster${RESET}"
else
    echo -e "Launching standalone single-broker KRaft container..."
    docker compose -f docker-compose.yml up -d
    echo -e "Waiting for Kafka broker to unfence and become healthy..."
    
    for i in {1..20}; do
        if docker compose -f docker-compose.yml ps | grep -q "healthy"; then
            echo -e "${GREEN}Kafka broker is online and healthy on port 9092!${RESET}"
            exit 0
        fi
        sleep 1
    done
    echo -e "${GREEN}Kafka broker is starting up; run 'docker compose ps' to inspect status.${RESET}"
fi
