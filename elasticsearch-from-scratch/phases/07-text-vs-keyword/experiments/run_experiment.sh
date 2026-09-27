#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 07: text vs keyword Experiments ==="
python3 phases/07-text-vs-keyword/code/text_vs_keyword_demo.py

echo -e "\n--- Testing Elasticsearch Mappings ---"
curl -s -X PUT "http://localhost:9200/demo_types" -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": { "keyword": { "type": "keyword" } }
      }
    }
  }
}' || true

curl -s -X PUT "http://localhost:9200/demo_types/_doc/1?refresh=true" -H "Content-Type: application/json" -d '{
  "title": "Distributed Systems"
}' || true

echo -e "\n1. Full-text match query on 'title':"
curl -s -X POST "http://localhost:9200/demo_types/_search" -H "Content-Type: application/json" -d '{
  "query": { "match": { "title": "distributed" } }
}' | grep -o '"total":{"value":[0-9]*' || true

echo -e "\n2. Exact term query on 'title.keyword':"
curl -s -X POST "http://localhost:9200/demo_types/_search" -H "Content-Type: application/json" -d '{
  "query": { "term": { "title.keyword": "Distributed Systems" } }
}' | grep -o '"total":{"value":[0-9]*' || true
