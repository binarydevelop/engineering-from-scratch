"""
Master runner for backend engineering performance benchmarks.
Executes all benchmarks and displays comparative analysis table.
"""

import sys
import os

BENCH_DIR = os.path.dirname(os.path.abspath(__file__))
if BENCH_DIR not in sys.path:
    sys.path.insert(0, BENCH_DIR)

import benchmark_sync_vs_async
import benchmark_connection_pooling
import benchmark_cache_aside
import benchmark_json_serialization
import benchmark_cursor_vs_offset

def main():
    print("=" * 80)
    print("      BACKEND ENGINEERING FROM SCRATCH — PERFORMANCE BENCHMARK SUITE")
    print("=" * 80)
    print()

    benchmarks = [
        benchmark_sync_vs_async.benchmark,
        benchmark_connection_pooling.benchmark,
        benchmark_cache_aside.benchmark,
        benchmark_json_serialization.benchmark,
        benchmark_cursor_vs_offset.benchmark,
    ]

    for bench_fn in benchmarks:
        result = bench_fn()
        print(f"▶ Benchmark: {result['name']}")
        for k, v in result.items():
            if k != "name":
                print(f"    • {k}: {v}")
        print("-" * 80)

    print()
    print("✔ All benchmarks completed successfully.")
    print("=" * 80)

if __name__ == "__main__":
    main()
