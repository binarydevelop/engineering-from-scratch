#!/usr/bin/env python3
import socket
import sys

def check_tcp(host, port):
    print(f"Testing TCP socket connection to {host}:{port}...")
    try:
        s = socket.create_connection((host, port), timeout=3)
        s.close()
        print(f" [OK] Successfully established TCP handshake with {host}:{port}")
        return True
    except Exception as e:
        print(f" [FAIL] Could not connect to {host}:{port}: {e}")
        return False

def check_kafka_metadata():
    print("Testing Kafka Cluster Metadata query via Python client...")
    try:
        from kafka import KafkaAdminClient
        admin = KafkaAdminClient(bootstrap_servers="localhost:9092", request_timeout_ms=3000)
        cluster_metadata = admin.describe_cluster()
        print(f" [OK] Cluster connection successful!")
        print(f"      Cluster ID: {cluster_metadata.get('cluster_id')}")
        print(f"      Controller ID: {cluster_metadata.get('controller_id')}")
        print(f"      Active Brokers: {len(cluster_metadata.get('brokers', []))}")
        admin.close()
        return True
    except Exception as e:
        print(f" [FAIL] Kafka metadata check failed: {e}")
        return False

if __name__ == "__main__":
    tcp_ok = check_tcp("localhost", 9092)
    if not tcp_ok:
        print("\nHint: Did you run 'make up' to start the Kafka container?")
        sys.exit(1)
    meta_ok = check_kafka_metadata()
    if meta_ok:
        print("\nEnvironment is fully operational!")
        sys.exit(0)
    else:
        sys.exit(1)
