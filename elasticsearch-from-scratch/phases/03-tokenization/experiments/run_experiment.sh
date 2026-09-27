#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 03: Tokenization Experiments ==="
python3 phases/03-tokenization/code/tokenizer_experiments.py

echo -e "\n--- Elasticsearch _analyze Standard Tokenizer ---"
curl -s -X POST "http://localhost:9200/_analyze" -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "text": "Redis, Kafka and Elasticsearch 8.17!"
}' | grep -o '"token":"[^"]*"' || echo "Elasticsearch offline."
