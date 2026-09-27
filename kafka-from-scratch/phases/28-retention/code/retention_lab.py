#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def test_retention():
    topic = "retention-lab"
    print(f"Producing records to topic '{topic}' with 5s retention...")
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    for i in range(200):
        producer.send(topic, value=b"data-to-be-retained-then-deleted")
    producer.flush()
    producer.close()
    print("Produced 200 records. Wait 10 seconds and check segment deletion inside container.")

if __name__ == "__main__":
    test_retention()
