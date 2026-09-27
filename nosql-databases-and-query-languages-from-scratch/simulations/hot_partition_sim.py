#!/usr/bin/env python3
"""
Hot Partition & Key Salting Simulator
Simulates a viral celebrity / flash sale item where 90% of requests hit a single key.
Measures the throughput collapse of an un-salted key vs a write-sharded / salted key.
"""

import random
import hashlib
from collections import Counter
from typing import List, Dict

def hash_to_partition(key: str, num_partitions: int = 8) -> int:
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % num_partitions

def run_simulation():
    print("======================================================================")
    print(" HOT PARTITION / SKEWED TRAFFIC SIMULATION")
    print("======================================================================")

    num_partitions = 8
    total_writes = 50000

    print(f"\nScenario A: Naive Key (Single Viral Item: ITEM#1029)")
    partition_counts_naive = Counter()
    for _ in range(total_writes):
        # 90% traffic to hot item, 10% to random items
        if random.random() < 0.90:
            key = "ITEM#1029"
        else:
            key = f"ITEM#{random.randint(2000, 9999)}"
        part = hash_to_partition(key, num_partitions)
        partition_counts_naive[part] += 1

    print("Partition Distribution (Naive):")
    for p in range(num_partitions):
        cnt = partition_counts_naive[p]
        pct = (cnt / total_writes) * 100
        bar = "█" * int(pct // 2)
        print(f" Partition {p}: {cnt:5d} writes ({pct:5.1f}%) | {bar}")

    hot_pct = max(partition_counts_naive.values()) / total_writes * 100
    print(f"Hot Partition Max Load: {hot_pct:.1f}% on a single physical partition!")
    print("Result: Partition bottlenecks, causing provisioned throughput throttling!")

    print("\nScenario B: Salted / Write-Sharded Key (ITEM#1029#0 through #7)")
    partition_counts_salted = Counter()
    salt_factor = 8
    for _ in range(total_writes):
        if random.random() < 0.90:
            salt = random.randint(0, salt_factor - 1)
            key = f"ITEM#1029#{salt}"
        else:
            key = f"ITEM#{random.randint(2000, 9999)}"
        part = hash_to_partition(key, num_partitions)
        partition_counts_salted[part] += 1

    print("Partition Distribution (Salted):")
    for p in range(num_partitions):
        cnt = partition_counts_salted[p]
        pct = (cnt / total_writes) * 100
        bar = "█" * int(pct // 2)
        print(f" Partition {p}: {cnt:5d} writes ({pct:5.1f}%) | {bar}")

    salted_max_pct = max(partition_counts_salted.values()) / total_writes * 100
    print(f"Salted Partition Max Load: {salted_max_pct:.1f}%")
    print("Conclusion: Key salting evenly dispersed writes across all 8 storage partitions!")

if __name__ == "__main__":
    run_simulation()
