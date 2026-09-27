#!/usr/bin/env python3

def calculate_shard_overhead(num_shards, heap_per_shard_mb=15):
    total_heap_mb = num_shards * heap_per_shard_mb
    total_heap_gb = total_heap_mb / 1024.0
    return total_heap_mb, total_heap_gb

if __name__ == "__main__":
    scenarios = [50, 500, 2000, 5000, 10000]
    print(f"{'Shard Count':15s} | {'Static Heap Consumed':25s} | {'Node Heap Impact (31GB Max)'}")
    print("-" * 75)
    for sc in scenarios:
        mb, gb = calculate_shard_overhead(sc)
        pct = (gb / 31.0) * 100
        print(f"{sc:15d} | {mb:6d} MB ({gb:5.1f} GB)          | {pct:5.1f}% of 31GB heap")
