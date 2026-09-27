#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 05: Analyzer Pipeline Experiments ==="
python3 phases/05-analyzer-pipeline/code/custom_analyzer_test.py

echo -e "\n--- Elasticsearch _analyze Custom Pipeline ---"
curl -s -X POST "http://localhost:9200/_analyze" -H "Content-Type: application/json" -d '{
  "char_filter": ["html_strip"],
  "tokenizer": "standard",
  "filter": ["lowercase", "stop"],
  "text": "<h2>Elasticsearch &amp; Lucene</h2> are <b>FAST</b>!"
}' | grep -o '"token":"[^"]*"' || echo "Elasticsearch offline."
