#!/usr/bin/env python3
import time
import subprocess
from kafka import KafkaProducer, KafkaConsumer

def run_production_lab():
    print("=== Capstone 3: Production-Like 3-Broker KRaft Lab ===\n")
    bootstrap = ["localhost:9092", "localhost:9094", "localhost:9096"]
    
    print("1. Connecting resilient producer (acks='all', retries=10)...")
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap,
            acks="all",
            retries=10,
            retry_backoff_ms=200
        )
        print(" [Producer OK] Connected to 3-broker cluster!")
        
        # Send 10 records
        for i in range(1, 11):
            f = producer.send("replicated-orders", key=b"cust-1", value=f"order-event-{i}".encode())
            meta = f.get(timeout=5)
            print(f"  Sent event {i:2d} -> Partition {meta.partition}, Offset {meta.offset}")
        producer.flush()
        producer.close()
        print("\nAll 10 records confirmed durable across cluster quorum!")
    except Exception as e:
        print(f"Error connecting to cluster: {e}")
        print("Hint: Did you launch the cluster with 'make up-cluster'?")

if __name__ == "__main__":
    run_production_lab()
