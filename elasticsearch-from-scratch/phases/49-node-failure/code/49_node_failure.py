#!/usr/bin/env python3
import time

def simulate_cluster_heartbeat(nodes_alive):
    primary_active = "node_1" in nodes_alive or "node_2" in nodes_alive
    replica_active = "node_1" in nodes_alive and "node_2" in nodes_alive

    if primary_active and replica_active:
        return "GREEN", "All primaries and replicas active."
    elif primary_active and not replica_active:
        return "YELLOW", "Primaries active; replica missing (redundancy degraded)."
    else:
        return "RED", "Primary shard offline! Data loss / search unavailability."

if __name__ == "__main__":
    states = [
        {"desc": "Normal Operation", "nodes": ["node_1", "node_2", "node_3"]},
        {"desc": "Node 1 Crashes (Primary lost, promoted replica)", "nodes": ["node_2", "node_3"]},
        {"desc": "Node 2 Crashes (All copies lost)", "nodes": ["node_3"]}
    ]
    for s in states:
        color, explanation = simulate_cluster_heartbeat(s["nodes"])
        print(f"Scenario: {s['desc']:50s} -> Health: [{color:6s}] - {explanation}")
