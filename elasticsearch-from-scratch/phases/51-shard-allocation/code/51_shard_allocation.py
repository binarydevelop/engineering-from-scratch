#!/usr/bin/env python3

def evaluate_allocation(node, shard):
    # Rule 1: Cannot place primary and replica on same node
    if shard["id"] in node["existing_shards"]:
        return False, "same_shard: node already hosts a copy of this shard"
    # Rule 2: Disk watermark
    if node["disk_usage_pct"] >= 85:
        return False, f"disk_threshold: node disk usage ({node['disk_usage_pct']}%) exceeds low watermark 85%"
    return True, "allocation allowed"

if __name__ == "__main__":
    node_a = {"name": "node-01", "disk_usage_pct": 50, "existing_shards": [0]}
    node_b = {"name": "node-02", "disk_usage_pct": 89, "existing_shards": []}
    shard = {"id": 0, "type": "replica"}

    print("Evaluating Shard Allocation for Replica Shard 0:")
    for n in [node_a, node_b]:
        allowed, reason = evaluate_allocation(n, shard)
        print(f"  Target: {n['name']} -> Allowed? {allowed} (Reason: {reason})")
