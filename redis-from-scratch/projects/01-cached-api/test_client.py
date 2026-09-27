#!/usr/bin/env python3
"""
projects/01-cached-api/test_client.py — Concurrency & Cache Stampede Load Tester
"""

import urllib.request
import json
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8080"

def fetch_product(prod_id):
    t0 = time.perf_counter()
    req = urllib.request.Request(f"{BASE_URL}/product/{prod_id}")
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode())
    latency_ms = (time.perf_counter() - t0) * 1000
    return body.get("_source"), latency_ms

def run_load_test(concurrency=30, requests_per_worker=5):
    print(f"Launching load test: {concurrency} concurrent threads requesting /product/prod_1...")
    
    sources = {}
    latencies = []
    
    def worker(_):
        res = []
        for _ in range(requests_per_worker):
            source, lat = fetch_product("prod_1")
            res.append((source, lat))
        return res

    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        all_results = pool.map(worker, range(concurrency))
        for thread_res in all_results:
            for source, lat in thread_res:
                sources[source] = sources.get(source, 0) + 1
                latencies.append(lat)
    total_time = time.perf_counter() - t_start

    print(f"\nCompleted {len(latencies)} requests in {total_time:.2f} seconds ({len(latencies)/total_time:,.0f} req/sec)")
    print("Breakdown by Data Source:")
    for src, count in sources.items():
        pct = (count / len(latencies)) * 100
        print(f"  • {src:35}: {count:4} ({pct:5.1f}%)")
    
    # Query metrics
    with urllib.request.urlopen(f"{BASE_URL}/metrics") as resp:
        m = json.loads(resp.read().decode())
    print("\nServer Metrics:")
    print(json.dumps(m, indent=2))

if __name__ == "__main__":
    run_load_test()
