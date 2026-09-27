#!/usr/bin/env python3

def evaluate_cluster_health(shards):
    # shards: list of dicts: {"shard": id, "type": "primary"|"replica", "assigned": bool}
    primaries = [s for s in shards if s["type"] == "primary"]
    replicas = [s for s in shards if s["type"] == "replica"]

    if not all(p["assigned"] for p in primaries):
        return "RED", "One or more primary shards are unassigned!"
    if not all(r["assigned"] for r in replicas):
        return "YELLOW", "All primaries active, but some replicas are unassigned."
    return "GREEN", "All primary and replica shards successfully assigned."

if __name__ == "__main__":
    test_shards = [
        {"shard": 0, "type": "primary", "assigned": True},
        {"shard": 0, "type": "replica", "assigned": False}
    ]
    status, reason = evaluate_cluster_health(test_shards)
    print(f"Cluster Status: [{status}]")
    print(f"Reason: {reason}")
