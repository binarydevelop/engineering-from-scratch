#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def bench_sync(n=200):
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    topic = "batch-bench-sync"
    start = time.time()
    for i in range(n):
        f = producer.send(topic, value=b"synchronous-payload-data")
        f.get(timeout=5) # Wait for every single record
    dur = time.time() - start
    producer.close()
    return n / dur, (dur / n) * 1000

def bench_batched(n=5000):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        linger_ms=20,
        batch_size=32768
    )
    topic = "batch-bench-async"
    start = time.time()
    for i in range(n):
        producer.send(topic, value=b"batched-payload-data")
    producer.flush() # Flush remaining
    dur = time.time() - start
    producer.close()
    return n / dur, (dur / n) * 1000

if __name__ == "__main__":
    print("Testing Synchronous Sends (1 by 1)...")
    sync_rps, sync_lat = bench_sync(200)
    print(f" -> Synchronous Throughput: {sync_rps:7.1f} rec/s | Avg Latency: {sync_lat:.2f} ms/rec")

    print("\nTesting Batched Asynchronous Sends (linger.ms=20, batch.size=32KB)...")
    async_rps, async_lat = bench_batched(5000)
    print(f" -> Batched Throughput:    {async_rps:7.1f} rec/s | Amortized Time: {async_lat:.3f} ms/rec")

    speedup = async_rps / sync_rps
    print(f"\nBatching Speedup Factor: {speedup:.1f}x faster!")
