#!/usr/bin/env python3
"""
benchmarks/benchmark_cache.py
Measures in-memory cache hit vs disk database query latency and demonstrates cache invalidation cost.
"""

import time
import statistics
from typing import Dict, Optional


class MockDatabase:
    def __init__(self, disk_seek_delay_ms: float = 12.0):
        self.disk_seek_delay_ms = disk_seek_delay_ms
        self.data = {f"user_{i}": f"User Profile Data {i}" for i in range(1000)}
        self.queries_served = 0

    def query(self, key: str) -> str:
        self.queries_served += 1
        time.sleep(self.disk_seek_delay_ms / 1000.0)
        return self.data.get(key, "")


class MockRedisCache:
    def __init__(self, memory_lookup_delay_ms: float = 0.5):
        self.memory_lookup_delay_ms = memory_lookup_delay_ms
        self.cache: Dict[str, str] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[str]:
        time.sleep(self.memory_lookup_delay_ms / 1000.0)
        val = self.cache.get(key)
        if val is not None:
            self.hits += 1
        else:
            self.misses += 1
        return val

    def set(self, key: str, val: str):
        self.cache[key] = val


def run_benchmark():
    print("=" * 65)
    print("      Cache-Aside (Redis) vs Direct Database Read Benchmark     ")
    print("=" * 65)

    db = MockDatabase(disk_seek_delay_ms=10.0)
    cache = MockRedisCache(memory_lookup_delay_ms=0.5)

    n_reads = 100
    test_key = "user_42"

    print(f"\nSimulating {n_reads} read operations for hot record '{test_key}'...")

    # Run without cache
    no_cache_latencies = []
    for _ in range(n_reads):
        t0 = time.perf_counter()
        _ = db.query(test_key)
        no_cache_latencies.append((time.perf_counter() - t0) * 1000.0)

    # Run with cache-aside
    with_cache_latencies = []
    for _ in range(n_reads):
        t0 = time.perf_counter()
        val = cache.get(test_key)
        if val is None:
            val = db.query(test_key)
            cache.set(test_key, val)
        with_cache_latencies.append((time.perf_counter() - t0) * 1000.0)

    print("\n--- Latency Comparison (Milliseconds) ---")
    print(f"Direct Database Reads: Mean={statistics.mean(no_cache_latencies):.2f}ms | Total Time={sum(no_cache_latencies):.1f}ms")
    print(f"Cache-Aside Reads:     Mean={statistics.mean(with_cache_latencies):.2f}ms | Total Time={sum(with_cache_latencies):.1f}ms")
    print(f"\nCache Hit Ratio: {cache.hits}/{n_reads} ({(cache.hits/n_reads)*100:.1f}%)")
    print(f"Database Queries Avoided: {n_reads - (db.queries_served - n_reads)}")

    speedup = statistics.mean(no_cache_latencies) / statistics.mean(with_cache_latencies)
    print(f"Effective Latency Speedup: {speedup:.1f}x faster with in-memory caching")
    print("=" * 65)


if __name__ == "__main__":
    run_benchmark()
