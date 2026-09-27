#!/usr/bin/env python3

def trace_write_lifecycle(doc_id, doc_body):
    return [
        f"1. Client POST /products/_doc/{doc_id}",
        f"2. Coordinating Node hashes ID -> Shard 1",
        f"3. Primary Shard validates mapping schema",
        f"4. Text Analyzer emits tokens: {doc_body.get('title', '').lower().split()}",
        f"5. Wrote terms to in-memory Indexing Buffer",
        f"6. Appended raw write to Translog on disk (Durability)",
        f"7. Dispatched write to Replica Shard on Node B",
        f"8. HTTP 201 Created returned to client",
        f"9. [T+1.0s] Refresh flushes buffer -> New Searchable Segment in OS Cache",
        f"10. [T+30m] Flush calls fsync() to disk -> Translog cleared",
        f"11. Background Tiered Merge consolidates segments & purges tombstones"
    ]

def trace_search_lifecycle(query_term):
    return [
        f"1. Client GET /products/_search?q={query_term}&size=10",
        f"2. Coordinating Node parses query and scatters to Shards [0, 1, 2]",
        f"3. Query Phase: Shards evaluate inverted index postings & BM25 scores",
        f"4. Each Shard returns its top 10 (DocID, BM25 Score) tuples",
        f"5. Coordinating Node priority-queue merges candidate lists -> Global Top 10",
        f"6. Fetch Phase: Coordinator requests _source only for 10 winning IDs",
        f"7. Shards decompress and return _source JSON",
        f"8. HTTP 200 OK returned to client with hits & facets"
    ]

if __name__ == "__main__":
    print("=== The Complete End-to-End Write Pipeline Trace ===")
    for step in trace_write_lifecycle("42", {"title": "Distributed Search Guide", "price": 49.99}):
        print(" ", step)

    print("\n=== The Complete End-to-End Search Pipeline Trace ===")
    for step in trace_search_lifecycle("distributed"):
        print(" ", step)
