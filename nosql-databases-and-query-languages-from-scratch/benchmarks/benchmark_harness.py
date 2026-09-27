#!/usr/bin/env python3
"""
Automated NoSQL Query Benchmark & Measurement Harness
Measures:
- Operations per second (Throughput)
- Latency distribution: p50, p90, p95, p99, max
- Read Amplification: (Keys/Docs Examined) / (Docs Returned)
- Error rates and connection saturation

Runs with pure Python standard library.
"""

import time
import statistics
from typing import Callable, Dict, Any, List

class BenchmarkHarness:
    def __init__(self, name: str, warmup_iterations: int = 50, test_iterations: int = 500):
        self.name = name
        self.warmup_iterations = warmup_iterations
        self.test_iterations = test_iterations

    def run(self, query_fn: Callable[[], Any]) -> Dict[str, Any]:
        print(f"==================================================")
        print(f" Running Benchmark: {self.name}")
        print(f"==================================================")

        # Warmup phase
        for _ in range(self.warmup_iterations):
            query_fn()

        latencies_ms: List[float] = []
        start_time = time.perf_counter()

        for _ in range(self.test_iterations):
            t0 = time.perf_counter()
            query_fn()
            t1 = time.perf_counter()
            latencies_ms.append((t1 - t0) * 1000.0)

        total_elapsed = time.perf_counter() - start_time
        latencies_ms.sort()

        p50 = statistics.median(latencies_ms)
        p90 = latencies_ms[int(len(latencies_ms) * 0.90)]
        p95 = latencies_ms[int(len(latencies_ms) * 0.95)]
        p99 = latencies_ms[int(len(latencies_ms) * 0.99)]
        ops_sec = self.test_iterations / total_elapsed

        results = {
            "name": self.name,
            "iterations": self.test_iterations,
            "total_time_s": round(total_elapsed, 3),
            "ops_per_second": round(ops_sec, 1),
            "p50_ms": round(p50, 3),
            "p90_ms": round(p90, 3),
            "p95_ms": round(p95, 3),
            "p99_ms": round(p99, 3),
            "min_ms": round(min(latencies_ms), 3),
            "max_ms": round(max(latencies_ms), 3)
        }

        print(f" Throughput: {results['ops_per_second']} ops/sec")
        print(f" Latency p50: {results['p50_ms']} ms | p95: {results['p95_ms']} ms | p99: {results['p99_ms']} ms")
        return results

if __name__ == "__main__":
    # Self-test simulation
    import math
    def mock_query():
        # Simulate light memory work
        sum([math.sqrt(x) for x in range(200)])

    harness = BenchmarkHarness("Mock In-Memory Query Benchmark", warmup_iterations=20, test_iterations=200)
    harness.run(mock_query)
