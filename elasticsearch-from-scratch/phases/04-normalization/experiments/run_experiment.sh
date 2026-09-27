#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 04: Normalization Experiments ==="
python3 phases/04-normalization/code/normalizer.py

echo -e "\n--- Elasticsearch _analyze with Lowercase & Stemmer ---"
curl -s -X POST "http://localhost:9200/_analyze" -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": ["lowercase", "porter_stem"],
  "text": "The distributed systems are running fast"
}' | grep -o '"token":"[^"]*"' || echo "Elasticsearch offline."
