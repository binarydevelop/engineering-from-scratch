#!/usr/bin/env python3

def simulate_search_phases(num_shards=5, page_size=10, doc_size_kb=50):
    # Eager approach: each shard returns full docs
    eager_bytes_kb = num_shards * page_size * doc_size_kb

    # Query-Then-Fetch:
    # Query phase: each shard returns (id, score) ≈ 16 bytes
    query_phase_bytes = (num_shards * page_size * 16) / 1024
    # Fetch phase: only page_size winning docs fetched
    fetch_phase_bytes = page_size * doc_size_kb
    qtf_total_kb = query_phase_bytes + fetch_phase_bytes

    return eager_bytes_kb, qtf_total_kb

if __name__ == "__main__":
    eager, qtf = simulate_search_phases(num_shards=10, page_size=10, doc_size_kb=100)
    print("Network Payload Comparison (10 Shards, size=10, 100KB doc body):")
    print(f"  Naive Eager Fetch:     {eager:8.1f} KB transferred across cluster")
    print(f"  Query-Then-Fetch:      {qtf:8.1f} KB transferred across cluster")
    print(f"  Bandwidth saved:       {((eager - qtf) / eager) * 100:.1f}%!")
