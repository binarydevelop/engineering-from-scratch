#!/usr/bin/env python3
import time

def simulate_fanout(num_shards, base_shard_latency_ms=1.5, per_shard_network_overhead_ms=0.3):
    # Simulated coordinator wait: max of shard latencies + merge cost
    import random
    random.seed(42)
    shard_times = [base_shard_latency_ms + random.uniform(0.1, 0.8) for _ in range(num_shards)]
    coordination_merge_time = num_shards * per_shard_network_overhead_ms
    total_time = max(shard_times) + coordination_merge_time
    return total_time

if __name__ == "__main__":
    print("Simulated Search Latency for 100MB Dataset across varying Shard Counts:\n")
    for s_count in [1, 2, 5, 10, 20, 50]:
        lat = simulate_fanout(s_count)
        print(f"  {s_count:2d} Primary Shards: {lat:6.2f} ms")
    print("\nNotice how coordination fan-out increases latency on small datasets!")
