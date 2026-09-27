#!/usr/bin/env python3
"""
Modulo Hash Partitioning vs Consistent Hashing Simulator
Demonstrates why simple modulo hash partitioning (hash(key) % N) causes catastrophic
data migration when scaling cluster nodes, and how Consistent Hashing with Virtual Nodes
minimizes key movement to exactly K / N keys.
"""

import hashlib
import bisect
from typing import Dict, List, Set

def modulo_hash(key: str, num_nodes: int) -> int:
    h = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
    return h % num_nodes

class ConsistentHashRing:
    def __init__(self, num_replicas: int = 100):
        self.num_replicas = num_replicas
        self.ring: List[int] = []
        self.ring_map: Dict[int, str] = {}
        self.nodes: Set[str] = set()

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str):
        self.nodes.add(node)
        for i in range(self.num_replicas):
            vnode_key = f"{node}#vnode{i}"
            h = self._hash(vnode_key)
            bisect.insort(self.ring, h)
            self.ring_map[h] = node

    def remove_node(self, node: str):
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        for i in range(self.num_replicas):
            vnode_key = f"{node}#vnode{i}"
            h = self._hash(vnode_key)
            idx = bisect.bisect_left(self.ring, h)
            if idx < len(self.ring) and self.ring[idx] == h:
                del self.ring[idx]
                del self.ring_map[h]

    def get_node(self, key: str) -> str:
        if not self.ring:
            raise ValueError("Hash ring is empty!")
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.ring_map[self.ring[idx]]

def run_simulation():
    num_keys = 10000
    keys = [f"customer_session_{i}" for i in range(num_keys)]

    print("======================================================================")
    print(" 1. MODULO HASH PARTITIONING: hash(key) % N")
    print("======================================================================")
    initial_nodes = 5
    mapping_initial = {k: modulo_hash(k, initial_nodes) for k in keys}

    new_nodes = 6
    mapping_scaled = {k: modulo_hash(k, new_nodes) for k in keys}

    moved_keys = sum(1 for k in keys if mapping_initial[k] != mapping_scaled[k])
    pct_moved = (moved_keys / num_keys) * 100
    print(f"Total Keys: {num_keys}")
    print(f"Nodes Scaled: {initial_nodes} ──> {new_nodes}")
    print(f"Keys Moved / Reshuffled: {moved_keys} ({pct_moved:.2f}%)")
    print(f"Conclusion: Simple modulo hashing forces ~{pct_moved:.1f}% of entire database to relocate across network!")

    print("\n======================================================================")
    print(" 2. CONSISTENT HASHING RING (with 150 vnodes per physical node)")
    print("======================================================================")
    ring = ConsistentHashRing(num_replicas=150)
    for i in range(initial_nodes):
        ring.add_node(f"node-{i}")

    ch_initial = {k: ring.get_node(k) for k in keys}

    # Add a 6th node to the ring
    ring.add_node("node-5")
    ch_scaled = {k: ring.get_node(k) for k in keys}

    ch_moved = sum(1 for k in keys if ch_initial[k] != ch_scaled[k])
    ch_pct_moved = (ch_moved / num_keys) * 100
    theoretical_optimal = (1 / new_nodes) * 100

    print(f"Total Keys: {num_keys}")
    print(f"Ring Scaled: {initial_nodes} nodes ──> {new_nodes} nodes")
    print(f"Keys Moved to new node: {ch_moved} ({ch_pct_moved:.2f}%)")
    print(f"Theoretical Optimal Movement (1/N): {theoretical_optimal:.2f}%")
    print(f"Conclusion: Consistent Hashing moved only ~{ch_pct_moved:.1f}% of keys! The remaining {100-ch_pct_moved:.1f}% remained untouched on their original nodes.")

if __name__ == "__main__":
    run_simulation()
