#!/usr/bin/env python3
import time

def trace_journey():
    stages = [
        ("1. Application Thread", "producer.send(topic='orders', key='user-42', value=...)", "< 1 µs"),
        ("2. Serializer", "Converts Key & Value to byte arrays", "10 µs"),
        ("3. Partitioner", "Murmur2Hash('user-42') % 3 = Partition 1", "5 µs"),
        ("4. RecordAccumulator", "Buffers into RecordBatch in memory (linger.ms / batch.size)", "1 - 20 ms"),
        ("5. Sender Thread", "Dispatches ProduceRequest over TCP socket to Broker 1", "1 - 2 ms"),
        ("6. Broker OS Page Cache", "Appends batch sequentially to orders-1/0000.log", "< 500 µs"),
        ("7. ISR Replication", "Followers fetch batch over TCP; Leader advances High Watermark", "2 - 5 ms"),
        ("8. Producer Ack", "Broker returns ProduceResponse: OK, Offset 42", "1 ms"),
        ("9. Consumer Fetch", "Consumer calls poll(); Broker streams via zero-copy sendfile()", "2 ms"),
        ("10. Business Processing", "Consumer processes event idempotently in DB", "10 - 50 ms"),
        ("11. Offset Commit", "Consumer commits Offset 43 to __consumer_offsets", "2 ms")
    ]

    print("=== Physical Lifecycle of a Single Kafka Record ===\n")
    print(f"{'Stage':<26} {'Action':<65} {'Approx Latency'}")
    print("-" * 105)
    for stage, action, lat in stages:
        print(f"{stage:<26} {action:<65} {lat}")
        time.sleep(0.05)

    print("\nKafka is no longer a black box.")
    print("Understand it. Build it. Measure it. Break it. Recover it. Scale it. Ship it.")

if __name__ == "__main__":
    trace_journey()
