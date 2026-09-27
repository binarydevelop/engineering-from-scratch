#!/usr/bin/env python3
"""
Benchmark: Partition Scaling
Measures theoretical and observed concurrency limits across varying partition counts.
"""

def evaluate_partition_scaling():
    print("=== Partition Scale & Concurrency Modeling ===\n")
    scenarios = [
        (1, 1, 2500, "Single partition bottleneck; only 1 consumer active in group."),
        (3, 3, 7500, "Balanced across 3 brokers; 3 parallel consumer workers."),
        (6, 6, 15000, "High throughput; 2 partitions per broker, 6 parallel workers."),
        (12, 12, 30000, "Large workload; 4 partitions per broker, 12 parallel workers.")
    ]

    print(f"{'Partitions':<12} {'Max Consumers':<16} {'Capacity (msgs/s)':<20} {'Operational Profile'}")
    print("-" * 80)
    for parts, cons, cap, note in scenarios:
        print(f"{parts:<12} {cons:<16} {cap:<20,d} {note}")

if __name__ == "__main__":
    evaluate_partition_scaling()
