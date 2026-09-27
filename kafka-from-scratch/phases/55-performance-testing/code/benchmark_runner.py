#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def run_performance_test(num_records=5000, payload_size=512):
    print(f"=== Running Kafka Performance Benchmark ({num_records} records, {payload_size} bytes each) ===\n")
    payload = b"B" * payload_size
    topic = "bench-perf-test"

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        acks=1,
        linger_ms=10,
        batch_size=32768
    )

    start = time.time()
    for _ in range(num_records):
        producer.send(topic, value=payload)
    producer.flush()
    duration = time.time() - start
    producer.close()

    total_bytes = num_records * payload_size
    rps = num_records / duration
    mb_s = (total_bytes / (1024 * 1024)) / duration
    avg_latency = (duration / num_records) * 1000

    print("Benchmark Results:")
    print(f"  Duration:          {duration:.3f} seconds")
    print(f"  Records/sec:       {rps:9.1f} rec/s")
    print(f"  Throughput (MB/s): {mb_s:9.2f} MB/s")
    print(f"  Amortized Latency: {avg_latency:9.3f} ms/record")

if __name__ == "__main__":
    run_performance_test()
