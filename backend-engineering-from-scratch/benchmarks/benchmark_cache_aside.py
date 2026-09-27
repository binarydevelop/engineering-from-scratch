"""
Benchmark: Cache Hit vs Database Query Latency.
Demonstrates the orders-of-magnitude performance gain of in-memory caching.
"""

import time
from typing import Dict, Any

def simulated_db_query(key: str) -> dict:
    # Simulate DB disk seek / parsing overhead (e.g., 0.2ms)
    time.sleep(0.0002)
    return {"key": key, "val": "payload_data"}

def benchmark() -> Dict[str, Any]:
    iterations = 500
    cache = {"item_key": {"key": "item_key", "val": "payload_data"}}

    # Database queries
    start_db = time.perf_counter()
    for _ in range(iterations):
        _ = simulated_db_query("item_key")
    db_duration = time.perf_counter() - start_db

    # Cache hits
    start_cache = time.perf_counter()
    for _ in range(iterations):
        _ = cache.get("item_key")
    cache_duration = time.perf_counter() - start_cache

    speedup = db_duration / cache_duration if cache_duration > 0 else 1.0

    return {
        "name": "Cache Hit vs Database Latency",
        "iterations": iterations,
        "database_time_sec": round(db_duration, 4),
        "cache_time_sec": round(cache_duration, 6),
        "speedup_ratio": round(speedup, 1)
    }

if __name__ == "__main__":
    res = benchmark()
    print(f"[{res['name']}]")
    print(f"  Database: {res['database_time_sec']}s")
    print(f"  Cache:    {res['cache_time_sec']}s")
    print(f"  Speedup:  {res['speedup_ratio']}x")
