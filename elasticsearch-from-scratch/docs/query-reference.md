# Elasticsearch 8.17.0 Query & REST API Reference

A practical cheatsheet for the essential endpoints, query DSL constructs, and administrative commands used throughout this repository.

---

## 1. Document Indexing & CRUD

### Create Index with Explicit Mappings
```bash
curl -X PUT http://localhost:9200/products -H "Content-Type: application/json" -d '{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "refresh_interval": "1s"
  },
  "mappings": {
    "properties": {
      "title": { "type": "text", "analyzer": "standard" },
      "category": { "type": "keyword" },
      "price": { "type": "double" },
      "in_stock": { "type": "boolean" },
      "created_at": { "type": "date" }
    }
  }
}'
```

### Index Document
```bash
curl -X PUT http://localhost:9200/products/_doc/1 -H "Content-Type: application/json" -d '{
  "title": "Ergonomic Mechanical Keyboard",
  "category": "peripherals",
  "price": 149.99,
  "in_stock": true,
  "created_at": "2026-01-15T09:00:00Z"
}'
```

### Bulk Ingestion (NDJSON format)
```bash
curl -X POST http://localhost:9200/_bulk -H "Content-Type: application/x-ndjson" -d '
{ "index": { "_index": "products", "_id": "2" } }
{ "title": "Ultra-wide 4K Monitor", "category": "monitors", "price": 499.0, "in_stock": true }
{ "index": { "_index": "products", "_id": "3" } }
{ "title": "Wireless Gaming Mouse", "category": "peripherals", "price": 79.5, "in_stock": false }
'
```

---

## 2. Query DSL

### Full-Text `match` Query
```bash
curl -X POST http://localhost:9200/products/_search -H "Content-Type: application/json" -d '{
  "query": {
    "match": {
      "title": "mechanical keyboard"
    }
  }
}'
```

### Exact Match & Range Filters (`term` & `range`)
```bash
curl -X POST http://localhost:9200/products/_search -H "Content-Type: application/json" -d '{
  "query": {
    "term": { "category": "peripherals" }
  }
}'
```

### Compound `bool` Query (Combining Relevance & Filters)
```bash
curl -X POST http://localhost:9200/products/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "wireless" } }
      ],
      "filter": [
        { "term": { "category": "peripherals" } },
        { "range": { "price": { "lte": 100.0 } } }
      ]
    }
  }
}'
```

### Phrase Search with Slop
```bash
curl -X POST http://localhost:9200/products/_search -H "Content-Type: application/json" -d '{
  "query": {
    "match_phrase": {
      "title": {
        "query": "mechanical keyboard",
        "slop": 1
      }
    }
  }
}'
```

---

## 3. Aggregations

### Bucket Terms Aggregation with Sub-Metric Aggregation
```bash
curl -X POST http://localhost:9200/products/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": { "field": "category", "size": 10 },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } },
        "max_price": { "max": { "field": "price" } }
      }
    }
  }
}'
```

---

## 4. Diagnostics & Cluster Introspection

```bash
# Cluster Health
curl -s http://localhost:9200/_cluster/health?pretty

# List Indices and Shard Counts
curl -s "http://localhost:9200/_cat/indices?v&s=index"

# Shard Locations across Nodes
curl -s "http://localhost:9200/_cat/shards?v&s=index,shard"

# Lucene Segments per Shard
curl -s "http://localhost:9200/_cat/segments/products?v"

# Explain Why Shard is Unassigned
curl -s http://localhost:9200/_cluster/allocation/explain?pretty

# Test Text Analyzer
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "analyzer": "standard",
  "text": "Elasticsearch 8.17 is distributed!"
}'
```
