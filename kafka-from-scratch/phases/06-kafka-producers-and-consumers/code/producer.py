#!/usr/bin/env python3
import time
import json
from kafka import KafkaProducer

def run_producer():
    print("Connecting KafkaProducer to localhost:9092...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all"
    )

    topic = "lab-orders"
    print(f"Producing 5 sample records to '{topic}'...")
    for i in range(1, 6):
        order = {
            "order_id": 1000 + i,
            "customer": f"user_{i}",
            "amount": round(19.99 * i, 2),
            "timestamp": time.time()
        }
        key = f"customer-{i}"
        future = producer.send(topic, key=key, value=order)
        # Block for acknowledgement to inspect metadata
        record_metadata = future.get(timeout=5)
        print(f" [Ack] Sent order {order['order_id']} -> Topic: {record_metadata.topic}, "
              f"Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")

    producer.flush()
    producer.close()
    print("Producer finished successfully.")

if __name__ == "__main__":
    run_producer()
