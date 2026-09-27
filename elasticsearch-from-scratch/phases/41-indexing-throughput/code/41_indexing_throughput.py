#!/usr/bin/env python3
import time

def benchmark_simulation():
    configurations = [
        {"name": "Naive (1 doc/req, refresh=1s, repl=1)", "rate": 250},
        {"name": "Batched (100 docs/req, refresh=1s, repl=1)", "rate": 2500},
        {"name": "Optimized (1000 docs/bulk, refresh=-1, repl=0)", "rate": 28000},
        {"name": "Max Concurrency (8 workers, bulk=1000, repl=0)", "rate": 65000}
    ]
    print(f"{'Configuration':50s} | {'Throughput (docs/sec)':25s}")
    print("-" * 80)
    for c in configurations:
        print(f"{c['name']:50s} | {c['rate']:10d} docs/sec")

if __name__ == "__main__":
    benchmark_simulation()
