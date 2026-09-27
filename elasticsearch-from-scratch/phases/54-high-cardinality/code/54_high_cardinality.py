#!/usr/bin/env python3
import time
import sys
from collections import defaultdict

def benchmark_cardinality_grouping(num_items, unique_values):
    data = [f"val_{i % unique_values}" for i in range(num_items)]
    t0 = time.perf_counter()
    counts = defaultdict(int)
    for v in data:
        counts[v] += 1
    elapsed = (time.perf_counter() - t0) * 1000
    memory_bytes = sys.getsizeof(counts)
    return elapsed, memory_bytes, len(counts)

if __name__ == "__main__":
    N = 200000
    print(f"Grouping {N} items by varying cardinality:\n")
    for u in [5, 100, 5000, 50000]:
        ms, mem, buckets = benchmark_cardinality_grouping(N, u)
        print(f"  Unique Values: {u:6d} -> Buckets: {buckets:6d} | Time: {ms:6.2f} ms | Hash Map RAM: {mem:8d} bytes")
