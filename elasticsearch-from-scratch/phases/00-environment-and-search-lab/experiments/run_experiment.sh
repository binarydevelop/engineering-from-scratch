#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 00 Experiment: Verifying Elasticsearch Lab ==="
python3 phases/00-environment-and-search-lab/code/check_node.py
curl -s http://localhost:9200/_cluster/health | grep -q "status" && echo "Cluster health check passed!"
