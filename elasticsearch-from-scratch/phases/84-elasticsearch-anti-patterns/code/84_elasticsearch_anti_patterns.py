#!/usr/bin/env python3

ANTIPATTERNS = [
    ("Primary Database", "Elasticsearch as sole primary ACID store", "Use PostgreSQL/MySQL as source of truth; sync to ES via CDC."),
    ("Oversharding", "Thousands of shards < 1GB", "Consolidate into shards sized 20GB to 50GB."),
    ("Dynamic Mapping", "dynamic: true allowing arbitrary JSON keys", "Enforce dynamic: strict and explicit schemas."),
    ("Leading Wildcards", "Executing *query* on large text", "Use edge_ngram or wildcard field type."),
    ("Deep Pagination", "from: 50000 with from + size", "Switch to search_after cursor pagination."),
    ("No Snapshots", "Zero backups relying only on replicas", "Configure automated daily snapshots to S3/GCS."),
    ("Heap Monopolization", "Allocating > 50% RAM or > 31GB to heap", "Cap heap at 50% of RAM (max 31GB) for OS page cache."),
    ("Unsecured Port", "Exposing port 9200 without TLS/auth", "Enable X-Pack security, TLS, and RBAC.")
]

if __name__ == "__main__":
    print("=== The Elasticsearch Anti-Pattern Audit ===\n")
    for idx, (title, symptom, remedy) in enumerate(ANTIPATTERNS, 1):
        print(f"Anti-Pattern {idx}: [{title}]")
        print(f"  Hazard: {symptom}")
        print(f"  Remedy: {remedy}\n")
