#!/usr/bin/env python3
from collections import defaultdict
import random

def simulate_traffic(num_shards=5, total_requests=10000, hot_shard_bias=0.7):
    # 70% of traffic goes to Shard 0 (e.g. VIP tenant)
    shard_load = defaultdict(int)
    for _ in range(total_requests):
        if random.random() < hot_shard_bias:
            shard_load[0] += 1
        else:
            s = random.randint(1, num_shards - 1)
            shard_load[s] += 1
    return shard_load

if __name__ == "__main__":
    random.seed(42)
    loads = simulate_traffic(num_shards=5, total_requests=10000, hot_shard_bias=0.75)
    print("Simulated Request Distribution across 5 Shards:")
    for s in range(5):
        pct = (loads[s] / 10000) * 100
        bar = "#" * int(pct // 2)
        print(f"  Shard [{s}]: {loads[s]:5d} requests ({pct:5.1f}%) | {bar}")
    print("\nShard 0 is a HOT SHARD absorbing 75% of total cluster work!")
