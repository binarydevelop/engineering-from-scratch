#!/usr/bin/env python3

class ClusterReplicaSim:
    def __init__(self):
        self.nodes = {
            "node_1": {"role": "primary", "alive": True, "docs": [1, 2, 3]},
            "node_2": {"role": "replica", "alive": True, "docs": [1, 2, 3]}
        }

    def search(self, query):
        # Round-robin across alive copies
        alive_nodes = [name for name, data in self.nodes.items() if data["alive"]]
        if not alive_nodes:
            raise RuntimeError("HTTP 503: Cluster Red - All shard copies offline!")
        chosen = alive_nodes[0]
        return f"Served from {chosen} ({self.nodes[chosen]['role']})"

    def kill_node(self, node_name):
        print(f"\n[CRASH] Killing {node_name}...")
        self.nodes[node_name]["alive"] = False
        # Master node failover detection
        if self.nodes[node_name]["role"] == "primary":
            for n, d in self.nodes.items():
                if d["alive"] and d["role"] == "replica":
                    d["role"] = "primary"
                    print(f"  [PROMOTION] Promoted {n} to PRIMARY shard!")

if __name__ == "__main__":
    cluster = ClusterReplicaSim()
    print("Initial state:", cluster.search("query 1"))
    cluster.kill_node("node_1")
    print("State after node_1 crash:", cluster.search("query 2"))
