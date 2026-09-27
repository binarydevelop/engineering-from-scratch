#!/usr/bin/env python3

FAILURES = [
    ("Node Crash", "Kill container hosting primary shard", "Master promotes replica; health YELLOW"),
    ("Queue Saturated", "Flood write pool with 50 threads", "HTTP 429 Too Many Requests"),
    ("Disk Flood Stage", "Simulate 96% disk watermark", "ClusterBlockException: read_only_allow_delete"),
    ("Mapping Explosion", "Dynamically index 2,000 unique keys", "total_fields.limit [1000] exceeded"),
    ("Circuit Breaker", "Run high-cardinality aggregation", "CircuitBreakingException: [parent] Data too large"),
    ("Unassigned Shard", "Set replicas=1 on single node", "same_shard decider blocks allocation"),
    ("Slow Regex Query", "Run unindexed broad wildcard", "Index search slow log triggered")
]

if __name__ == "__main__":
    print("=== The 7 Canonical Search Failure Modes ===\n")
    for idx, (name, trigger, outcome) in enumerate(FAILURES, 1):
        print(f"Drill {idx}: [{name:18s}]")
        print(f"  Trigger: {trigger}")
        print(f"  Outcome: {outcome}\n")
