#!/usr/bin/env python3
"""
Hash Partitioning & Token Ring Distribution Simulator
Demonstrates how distributed storage engines distribute key ranges across physical partitions,
and how range partitioning differs from hash partitioning.
"""

import hashlib
from collections import Counter
from typing import Dict, List, Tuple

def md5_hash_int(key: str) -> int:
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

def run_simulation():
    print("======================================================================")
    print(" HASH PARTITIONING & TOKEN RING SIMULATION")
    print("======================================================================")

    num_partitions = 4
    num_keys = 20000

    print(f"\n1. Uniform Hash Distribution: {num_keys} keys across {num_partitions} partitions")
    partition_counts = Counter()
    for i in range(num_keys):
        key = f"user_account_{i:06d}"
        partition_id = md5_hash_int(key) % num_partitions
        partition_counts[partition_id] += 1

    expected_per_partition = num_keys // num_partitions
    print(f"Target uniform capacity per partition: {expected_per_partition} keys (25.0%)")

    for p in range(num_partitions):
        cnt = partition_counts[p]
        pct = (cnt / num_keys) * 100
        delta = cnt - expected_per_partition
        delta_pct = (delta / expected_per_partition) * 100
        print(f" Partition {p}: {cnt:5d} keys ({pct:5.2f}%) [Variance: {delta_pct:+.2f}%]")

    print("\n2. Range Partitioning vs Hash Partitioning Comparison:")
    print(" Range Partitioning (e.g. key ranges A-F, G-M, N-S, T-Z):")
    print("  + Enables single-partition range queries across keys")
    print("  - Vulnerable to write hotspots (e.g. all sequential auto-increment keys hit the last partition)")
    print(" Hash Partitioning (e.g. MD5 / Murmur3 hash token):")
    print("  + Guarantees uniform random distribution across cluster nodes")
    print("  - Disperses contiguous keys randomly; range queries across keys require scatter-gather broadcast")

if __name__ == "__main__":
    run_simulation()
