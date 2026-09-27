#!/usr/bin/env python3
"""
Benchmark: Throughput vs Latency
Measures producer throughput and p50, p95, p99 latency across different batch sizes and linger settings.
"""

import time
import statistics
from kafka import KafkaProducer

def run_bench(linger_ms=10, batch_size=32768, num_records=2000):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        linger_ms=linger_ms,
        batch_size=batch_size,
        acks=1
    )
    topic = "bench-throughput-latency"
    payload = b"X" * 256

    latencies = []
    start_total = time.time()
    for _ in range(num_records):
        t0 = time.time()
        f = producer.send(topic, value=payload)
        latencies.append((time.time() - t0) * 1000)

    producer.flush()
    total_time = time.time() - start_total
    producer.close()

    rps = num_records / total_time
    mb_s = (num_records * 256 / (1024 * 1024)) / total_time
    p50 = statistics.median(latencies)
    p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else p50
    p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else p95

    return {
        "linger_ms": linger_ms,
        "batch_size": batch_size,
        "rps": rps,
        "mb_s": mb_s,
        "p50": p50,
        "p95": p95,
        "p99": p99
    }

if __name__ == "__main__":
    print("=== Running Producer Throughput & Latency Benchmark ===\n")
    results = [
        run_bench(linger_ms=0, batch_size=16384, num_records=2000),
        run_bench(linger_ms=10, batch_size=32768, num_records=2000),
        run_bench(linger_ms=20, batch_size=65536, num_records=2000)
    ]
    print(f"{'Linger (ms)':<12} {'Batch (KB)':<12} {'Throughput (rec/s)':<20} {'MB/s':<10} {'p50 (ms)':<10} {'p99 (ms)'}")
    print("-" * 75)
    for r in results:
        print(f"{r['linger_ms']:<12} {r['batch_size']//1024:<12} {r['rps']:<20.1f} {r['mb_s']:<10.2f} {r['p50']:<10.3f} {r['p99']:.3f}")
