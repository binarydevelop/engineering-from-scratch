#!/usr/bin/env python3
"""
experiments/hot_partition_lab.py
Phase 31: DynamoDB Capacity, Partition Hashing, and Hot Partitions

This lab demonstrates the fundamental physics of distributed key-value storage:
  1. Consistent Hashing: How partition keys map to internal storage nodes.
  2. The Hot Partition Trap: How choosing a low-cardinality key (e.g., Status or Date)
     causes 95% of traffic to hammer a single partition, triggering throttling (HTTP 400 ProvisionedThroughputExceededException)
     even when 80% of total provisioned capacity is completely idle.
  3. Key Salting & High-Cardinality Design: Distributing traffic evenly to achieve 100% throughput.
"""

import hashlib
from typing import Dict, List, Tuple


class StoragePartition:
    def __init__(self, partition_id: int, max_wcu: int = 1000):
        self.partition_id = partition_id
        self.max_wcu = max_wcu
        self.current_writes = 0
        self.throttled_requests = 0

    def write_item(self) -> bool:
        if self.current_writes >= self.max_wcu:
            self.throttled_requests += 1
            return False  # Throttled!
        self.current_writes += 1
        return True

    def reset_interval(self):
        self.current_writes = 0
        self.throttled_requests = 0


class DistributedTable:
    def __init__(self, num_partitions: int = 4, partition_capacity: int = 1000):
        self.num_partitions = num_partitions
        self.partitions = [StoragePartition(i, partition_capacity) for i in range(num_partitions)]
        self.total_capacity = num_partitions * partition_capacity

    def get_partition(self, partition_key: str) -> StoragePartition:
        # Internal DynamoDB hashing primitive: MD5 hash modulo partition count
        hash_val = int(hashlib.md5(partition_key.encode('utf-8')).hexdigest(), 16)
        partition_idx = hash_val % self.num_partitions
        return self.partitions[partition_idx]

    def put_item(self, partition_key: str) -> bool:
        partition = self.get_partition(partition_key)
        return partition.write_item()

    def get_stats(self) -> List[Tuple[int, int, int]]:
        return [(p.partition_id, p.current_writes, p.throttled_requests) for p in self.partitions]

    def reset(self):
        for p in self.partitions:
            p.reset_interval()


def run_experiment():
    print("=" * 65)
    print("   DynamoDB Partition Hashing & Hot Partition Simulation Lab     ")
    print("=" * 65)

    table = DistributedTable(num_partitions=4, partition_capacity=1000)
    print(f"Provisioned Capacity: {table.total_capacity} WCU distributed across {table.num_partitions} partitions (1,000 WCU each).")

    # Anti-Pattern Experiment: Skewed Partition Key
    print("\n--- Experiment 1: The Anti-Pattern (Status as Partition Key) ---")
    print("Scenario: A flash sale where 3,000 orders are written with PK='PENDING'.")

    table.reset()
    successful_writes = 0
    throttled_writes = 0

    for _ in range(3000):
        if table.put_item(partition_key="PENDING"):
            successful_writes += 1
        else:
            throttled_writes += 1

    print("\nPartition Utilization Stats:")
    for pid, writes, throttles in table.get_stats():
        bar = "█" * (writes // 50)
        print(f"  Partition {pid}: {writes:4d}/1000 WCU [{bar:<20}] (Throttled: {throttles})")

    print(f"\nOverall Result:")
    print(f"  Total Requested: 3,000 writes/sec")
    print(f"  Successful:      {successful_writes} writes/sec")
    print(f"  Throttled:       {throttled_writes} writes/sec (HTTP 400 ProvisionedThroughputExceededException)")
    print("Key Insight: Even though the table had 4,000 total provisioned WCU, 2,000 requests were throttled")
    print("because 3 partitions were at 0% utilization while 1 partition was 100% saturated!")

    # Well-Architected Solution: High Cardinality & Salted Key
    print("\n--- Experiment 2: Well-Architected Pattern (High Cardinality PK) ---")
    print("Scenario: Writing 3,000 orders with PK='ORDER#<uuid>' (evenly distributed).")

    table.reset()
    successful_writes = 0
    throttled_writes = 0

    for i in range(3000):
        pk = f"ORDER#{i:06d}"
        if table.put_item(partition_key=pk):
            successful_writes += 1
        else:
            throttled_writes += 1

    print("\nPartition Utilization Stats:")
    for pid, writes, throttles in table.get_stats():
        bar = "█" * (writes // 50)
        print(f"  Partition {pid}: {writes:4d}/1000 WCU [{bar:<20}] (Throttled: {throttles})")

    print(f"\nOverall Result:")
    print(f"  Total Requested: 3,000 writes/sec")
    print(f"  Successful:      {successful_writes} writes/sec")
    print(f"  Throttled:       {throttled_writes} writes/sec")
    assert throttled_writes == 0, "No writes should be throttled under uniform distribution!"
    print("Key Insight: Uniform partition key distribution unlocked 100% of provisioned throughput with 0% throttling.")

    print("\n" + "=" * 65)
    print("First-Principles Realization:")
    print("A distributed database does not automatically balance application traffic.")
    print("Partition keys must have high cardinality to avoid physical hot spots.")
    print("=" * 65)


if __name__ == "__main__":
    run_experiment()
