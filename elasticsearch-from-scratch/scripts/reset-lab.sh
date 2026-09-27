#!/usr/bin/env bash
# ==============================================================================
# reset-lab.sh - Wipe indices and reset laboratory environment to clean state
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "Resetting Elasticsearch lab state..."

if curl -s http://localhost:9200/_cluster/health &>/dev/null; then
    echo "Elasticsearch is reachable. Deleting all user indices..."
    # Delete all indices except system indices starting with .
    INDICES=$(curl -s "http://localhost:9200/_cat/indices?h=index" | grep -v '^\.' || true)
    if [ -n "$INDICES" ]; then
        for idx in $INDICES; do
            echo "Deleting index: $idx"
            curl -s -X DELETE "http://localhost:9200/$idx" > /dev/null || true
        done
    else
        echo "No user indices found."
    fi

    # Reset any cluster settings blocks (like read_only_allow_delete)
    echo "Resetting cluster settings..."
    curl -s -X PUT "http://localhost:9200/_cluster/settings" -H "Content-Type: application/json" -d '{
      "transient": {
        "cluster.routing.allocation.enable": "all"
      }
    }' > /dev/null || true
else
    echo "Elasticsearch is not running on localhost:9200. Tearing down any leftover containers and volumes..."
    docker compose -f docker-compose.yml down -v --remove-orphans 2>/dev/null || true
    docker compose -f docker-compose.cluster.yml down -v --remove-orphans 2>/dev/null || true
fi

# Clean local scratch and cache directories
rm -rf outputs/temp_* outputs/benchmark_*.json __pycache__ tests/__pycache__

echo "Lab reset successfully completed."
