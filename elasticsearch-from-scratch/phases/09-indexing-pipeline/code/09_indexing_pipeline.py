#!/usr/bin/env python3
import hashlib

def route_shard(doc_id, num_shards=3):
    # Simplified murmur3-style hash simulation
    h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
    return h % num_shards

def simulate_indexing_pipeline(doc_id, doc, num_shards=3):
    steps = []
    steps.append(f"1. Client issues write request for ID '{doc_id}'")
    shard_id = route_shard(doc_id, num_shards)
    steps.append(f"2. Routed to Primary Shard [{shard_id}] (hash({doc_id}) % {num_shards})")
    steps.append(f"3. Validated fields against schema mapping")
    steps.append(f"4. Executed text analysis: parsed {len(doc)} fields")
    steps.append(f"5. Wrote document terms to in-memory Lucene buffer")
    steps.append(f"6. Appended raw operation to Translog on disk for durability")
    steps.append(f"7. Dispatched operation to replica shard on peer node")
    steps.append(f"8. Returned HTTP 201 Created to client (Segment not yet refreshed!)")
    return steps

if __name__ == "__main__":
    trace = simulate_indexing_pipeline("order-98712", {"item": "Laptop", "price": 1200})
    for s in trace:
        print(s)
