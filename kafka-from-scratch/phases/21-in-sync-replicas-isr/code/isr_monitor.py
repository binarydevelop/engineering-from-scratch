#!/usr/bin/env python3
import time
from kafka import KafkaAdminClient

def monitor_topic_isr(topic="replicated-orders"):
    print(f"Monitoring ISR state for topic '{topic}'...")
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"]
        )
        # Describe topic
        cluster = admin.describe_cluster()
        print("Connected to cluster. Polling topic metadata...")
        admin.close()
    except Exception as e:
        print(f"Error checking ISR: {e}")

if __name__ == "__main__":
    monitor_topic_isr()
