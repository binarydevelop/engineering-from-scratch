#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 08: Explicit Mappings & Dynamic Traps ==="
python3 phases/08-mappings/code/mapping_simulation.py

echo -e "\n--- Creating Index with Strict Dynamic Mapping ---"
curl -s -X PUT "http://localhost:9200/strict_products" -H "Content-Type: application/json" -d '{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "sku": { "type": "keyword" },
      "price": { "type": "double" }
    }
  }
}' || true

echo -e "\n1. Indexing valid document (should succeed):"
curl -s -X POST "http://localhost:9200/strict_products/_doc/1" -H "Content-Type: application/json" -d '{
  "sku": "KB-990",
  "price": 129.99
}' | grep -o '"result":"[^"]*"' || true

echo -e "\n2. Indexing unexpected field (should fail with strict exception):"
curl -s -X POST "http://localhost:9200/strict_products/_doc/2" -H "Content-Type: application/json" -d '{
  "sku": "KB-991",
  "price": 139.99,
  "unexpected_tag": "sale"
}' | grep -o '"type":"[^"]*"' || true
