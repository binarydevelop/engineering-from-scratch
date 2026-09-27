#!/usr/bin/env bash
# ==============================================================================
# start-elasticsearch.sh - Launch single-node or 3-node Elasticsearch lab
# ==============================================================================
set -euo pipefail

MODE="${1:-single}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

if [ "$MODE" = "cluster" ]; then
    echo "Starting 3-Node Elasticsearch Cluster Lab (es01, es02, es03)..."
    docker compose -f docker-compose.cluster.yml up -d
    COMPOSE_FILE="docker-compose.cluster.yml"
else
    echo "Starting Single-Node Elasticsearch Lab (es-lab-01)..."
    docker compose -f docker-compose.yml up -d
    COMPOSE_FILE="docker-compose.yml"
fi

echo -n "Waiting for Elasticsearch to become responsive at http://localhost:9200..."
MAX_ATTEMPTS=45
ATTEMPT=0

until curl -s http://localhost:9200/_cluster/health &>/dev/null; do
    ATTEMPT=$((ATTEMPT + 1))
    if [ "$ATTEMPT" -ge "$MAX_ATTEMPTS" ]; then
        echo -e "\nError: Elasticsearch did not become ready within 45 seconds."
        echo "Check logs using: docker compose -f $COMPOSE_FILE logs"
        exit 1
    fi
    echo -n "."
    sleep 1
done

echo ""
HEALTH=$(curl -s http://localhost:9200/_cluster/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "ready")
echo "Elasticsearch is ONLINE! Cluster status: $HEALTH"
curl -s http://localhost:9200/ | grep -E 'name|cluster_name|number|lucene_version' || true
