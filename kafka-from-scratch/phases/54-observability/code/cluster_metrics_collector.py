#!/usr/bin/env python3
def display_golden_metrics():
    print("=== The 6 Golden Metrics of Apache Kafka Observability ===\n")
    metrics = [
        ("OfflinePartitionsCount", "0", "CRITICAL", "Partitions with no leader. Read/write completely halted!"),
        ("UnderReplicatedPartitions", "0", "CRITICAL", "Partitions where ISR < Replication Factor. Durability at risk!"),
        ("ActiveControllerCount", "1", "CRITICAL", "Exactly 1 active KRaft controller must exist. If 0, metadata frozen."),
        ("IsrShrinksPerSec", "0.0", "WARNING", "Replicas falling out of sync due to GC pauses or network latency."),
        ("ConsumerLag (per partition)", "< 1,000", "WARNING", "Downstream processing falling behind real-time production."),
        ("DiskUsagePercentage", "< 75%", "WARNING", "Broker disk saturation indicator.")
    ]

    print(f"{'Metric Name':<28} {'Healthy Target':<16} {'Severity':<10} {'Operational Meaning'}")
    print("-" * 85)
    for name, target, sev, desc in metrics:
        print(f"{name:<28} {target:<16} {sev:<10} {desc}")

if __name__ == "__main__":
    display_golden_metrics()
