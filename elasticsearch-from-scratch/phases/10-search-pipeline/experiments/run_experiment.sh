#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 10: Search Pipeline Simulation ==="
python3 phases/10-search-pipeline/code/search_pipeline_trace.py

echo -e "\n--- Running Search on Elasticsearch ---"
curl -s -X POST "http://localhost:9200/trace_demo/_search" -H "Content-Type: application/json" -d '{
  "query": { "match_all": {} },
  "size": 2
}' | grep -o '"hits":\[.*\]' || true
