#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 09: Indexing Pipeline Trace ==="
python3 phases/09-indexing-pipeline/code/trace_indexing.py

echo -e "\n--- Inspecting Translog Stats from Elasticsearch ---"
curl -s -X POST "http://localhost:9200/trace_demo/_doc/1" -H "Content-Type: application/json" -d '{"msg": "trace payload"}' || true
curl -s "http://localhost:9200/trace_demo/_stats/translog?pretty" | grep -E 'operations|size_in_bytes' || true
