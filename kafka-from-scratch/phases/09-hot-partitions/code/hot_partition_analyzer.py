#!/usr/bin/env python3
import random
import zlib
from collections import Counter

def get_partition(key: str, num_partitions: int = 4) -> int:
    return (zlib.crc32(key.encode("utf-8")) & 0x7fffffff) % num_partitions

def run_skew_simulation(total_records=10000, skew_ratio=0.90):
    print(f"Simulating {total_records} records with {int(skew_ratio*100)}% traffic skew...")
    counts = Counter()

    for _ in range(total_records):
        if random.random() < skew_ratio:
            key = "HOT_CUSTOMER_NIKE"
        else:
            key = f"small_customer_{random.randint(1, 100)}"
        part = get_partition(key, num_partitions=4)
        counts[part] += 1

    print("\nPartition Traffic Distribution:")
    for p in range(4):
        pct = (counts[p] / total_records) * 100
        bar = "█" * int(pct // 2)
        print(f" Partition {p}: {counts[p]:5d} msgs ({pct:5.1f}%) | {bar}")

if __name__ == "__main__":
    run_skew_simulation()
