#!/usr/bin/env python3
"""
benchmarks/benchmark_lb.py
Measures direct server latency vs reverse proxy load-balanced latency under concurrency.
"""

import time
import statistics
import concurrent.futures
from typing import List, Tuple


def mock_server_handle(delay_ms: float = 5.0) -> float:
    start = time.perf_counter()
    time.sleep(delay_ms / 1000.0)
    return (time.perf_counter() - start) * 1000.0


def mock_lb_forward(delay_ms: float = 5.0, proxy_overhead_ms: float = 0.8) -> float:
    start = time.perf_counter()
    # Proxy Layer 7 parsing + connection overhead
    time.sleep(proxy_overhead_ms / 1000.0)
    # Forward to target
    time.sleep(delay_ms / 1000.0)
    return (time.perf_counter() - start) * 1000.0


def run_benchmark():
    print("=" * 65)
    print("        Load Balancer vs Direct Target Latency Benchmark        ")
    print("=" * 65)

    n_requests = 100
    concurrency = 10

    print(f"\nSimulating {n_requests} requests across {concurrency} concurrent threads...")

    # Benchmark 1: Direct Target
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        direct_latencies = list(executor.map(lambda _: mock_server_handle(5.0), range(n_requests)))

    # Benchmark 2: Through Load Balancer (ALB)
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        lb_latencies = list(executor.map(lambda _: mock_lb_forward(5.0, 0.8), range(n_requests)))

    print("\n--- Latency Breakdown (Milliseconds) ---")
    print(f"Direct Target:    p50={statistics.median(direct_latencies):.2f}ms | p95={statistics.quantiles(direct_latencies, n=20)[18]:.2f}ms | Mean={statistics.mean(direct_latencies):.2f}ms")
    print(f"Via Reverse Proxy: p50={statistics.median(lb_latencies):.2f}ms | p95={statistics.quantiles(lb_latencies, n=20)[18]:.2f}ms | Mean={statistics.mean(lb_latencies):.2f}ms")

    overhead = statistics.mean(lb_latencies) - statistics.mean(direct_latencies)
    print(f"\nMeasured Reverse Proxy Overhead: +{overhead:.2f}ms")
    print("Key Tradeoff: The load balancer introduces a sub-millisecond hop penalty in exchange")
    print("for horizontal elasticity, multi-AZ high availability, and automated health checks.")
    print("=" * 65)


if __name__ == "__main__":
    run_benchmark()
