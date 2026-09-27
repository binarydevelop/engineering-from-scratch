#!/usr/bin/env python3
from kafka import KafkaAdminClient

def inspect_cluster():
    print("Connecting to Kafka cluster at localhost:9092, localhost:9094, localhost:9096...")
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"],
            request_timeout_ms=3000
        )
        metadata = admin.describe_cluster()
        brokers = metadata.get("brokers", [])
        print(f"\nConnected Brokers ({len(brokers)} total):")
        for b in brokers:
            print(f"  Broker ID: {b.get('node_id')} at {b.get('host')}:{b.get('port')}")
        admin.close()
    except Exception as e:
        print(f"Cluster connection error: {e}")
        print("Hint: Did you launch the 3-broker cluster with 'make up-cluster'?")

if __name__ == "__main__":
    inspect_cluster()
