#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def run_resilient_producer():
    print("Starting resilient producer with retries enabled...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"],
        acks="all",
        retries=10,
        retry_backoff_ms=200
    )
    topic = "failover-orders"
    print("Continuously publishing records. Kill a broker to observe failover...")
    for i in range(1, 21):
        try:
            future = producer.send(topic, key=b"k1", value=f"msg-{i}".encode())
            meta = future.get(timeout=10)
            print(f" [Sent] Msg {i:2d} -> Partition {meta.partition} on Broker {meta.offset}")
            time.sleep(0.3)
        except Exception as e:
            print(f" [RETRYING] Exception during send: {e}")
            time.sleep(0.5)

    producer.close()
    print("Producer finished successfully.")

if __name__ == "__main__":
    run_resilient_producer()
