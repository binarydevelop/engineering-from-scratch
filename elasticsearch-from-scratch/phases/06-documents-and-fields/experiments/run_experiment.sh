#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 06: Fielded Document Indexing ==="
python3 phases/06-documents-and-fields/code/fielded_search.py

echo -e "\n--- Indexing to Elasticsearch ---"
curl -s -X PUT "http://localhost:9200/products_phase06/_doc/1" -H "Content-Type: application/json" -d '{
  "title": "Ergonomic Office Chair",
  "price": 299.99,
  "category": "furniture"
}' || echo "ES offline"

curl -s "http://localhost:9200/products_phase06/_doc/1?pretty" || true
