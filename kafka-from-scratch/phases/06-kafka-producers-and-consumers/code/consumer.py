#!/usr/bin/env python3
import json
from kafka import KafkaConsumer

def run_consumer():
    print("Connecting KafkaConsumer to localhost:9092...")
    consumer = KafkaConsumer(
        "lab-orders",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=5000, # Stop if no records for 5s
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("Consuming records from 'lab-orders':")
    count = 0
    for record in consumer:
        count += 1
        print(f" [Record] Partition: {record.partition}, Offset: {record.offset}, "
              f"Key: {record.key}, Value: {record.value}")

    consumer.close()
    print(f"Consumed {count} records.")

if __name__ == "__main__":
    run_consumer()
