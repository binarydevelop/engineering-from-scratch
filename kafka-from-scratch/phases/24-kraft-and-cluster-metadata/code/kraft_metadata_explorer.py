#!/usr/bin/env python3
from kafka import KafkaAdminClient

def check_kraft_info():
    print("Querying KRaft Cluster Metadata...")
    admin = KafkaAdminClient(bootstrap_servers=["localhost:9092"])
    cluster_info = admin.describe_cluster()
    print(f"  Cluster ID:    {cluster_info.get('cluster_id')}")
    print(f"  Controller ID: {cluster_info.get('controller_id')}")
    brokers = cluster_info.get('brokers', [])
    print(f"  Brokers Count: {len(brokers)}")
    for b in brokers:
        print(f"    - Broker ID {b.get('node_id')}: {b.get('host')}:{b.get('port')}")
    admin.close()

if __name__ == "__main__":
    check_kraft_info()
