#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def trigger_segment_rolls(topic="rolling-lab", num_records=300):
    print(f"Producing {num_records} records to '{topic}' to trigger segment rolls...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        linger_ms=0 # Send immediately
    )
    # 256 bytes payload
    payload = b"A" * 256
    for i in range(num_records):
        producer.send(topic, value=payload)
    producer.flush()
    producer.close()
    print("Finished producing. Check container filesystem for multiple segment files!")

if __name__ == "__main__":
    trigger_segment_rolls()
