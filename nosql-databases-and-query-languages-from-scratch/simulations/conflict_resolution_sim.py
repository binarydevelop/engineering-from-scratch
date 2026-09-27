#!/usr/bin/env python3
"""
Conflict Resolution Simulator: Last-Write-Wins (LWW) vs Vector Clocks
Demonstrates why physical clock drift (NTP skew) causes Last-Write-Wins to silently
destroy data, and how Vector Clocks reliably detect concurrent conflicting updates.
"""

import time
from typing import Dict, Tuple, List, Optional

class VectorClock:
    def __init__(self, clock_dict: Optional[Dict[str, int]] = None):
        self.clock: Dict[str, int] = dict(clock_dict) if clock_dict else {}

    def increment(self, node_id: str):
        self.clock[node_id] = self.clock.get(node_id, 0) + 1

    def clone(self) -> 'VectorClock':
        return VectorClock(self.clock)

    def dominates(self, other: 'VectorClock') -> bool:
        """Returns True if self causally dominates (succeeded) other"""
        at_least_one_greater = False
        all_keys = set(self.clock.keys()).union(set(other.clock.keys()))
        for k in all_keys:
            v_self = self.clock.get(k, 0)
            v_other = other.clock.get(k, 0)
            if v_self < v_other:
                return False
            if v_self > v_other:
                at_least_one_greater = True
        return at_least_one_greater

    def is_concurrent(self, other: 'VectorClock') -> bool:
        return not self.dominates(other) and not other.dominates(self) and (self.clock != other.clock)

    def __repr__(self):
        return str(sorted(self.clock.items()))

def run_simulation():
    print("======================================================================")
    print(" 1. LAST-WRITE-WINS (LWW) WITH CLOCK DRIFT FAILURE")
    print("======================================================================")

    # Real chronological time:
    # t=100: Client A writes "item_count = 10" on Node 1
    # t=105: Client B writes "item_count = 25" on Node 2 (later in real time!)
    # But Node 2's physical clock is drifting backwards by 15ms (clock skew):
    node1_timestamp = 100.0
    node2_timestamp = 105.0 - 15.0  # Node 2 thinks it is t=90.0!

    print(f"Real Time: Client A wrote at t=100.0, Client B wrote at t=105.0")
    print(f"Recorded Timestamps: Node 1={node1_timestamp}, Node 2={node2_timestamp}")

    # LWW picks higher timestamp:
    lww_winner = "Node 1 (A)" if node1_timestamp > node2_timestamp else "Node 2 (B)"
    print(f"LWW Resolution Winner: {lww_winner}")
    print(f"Result: Client B's newer mutation was SILENTLY LOST due to 15ms clock drift!")

    print("\n======================================================================")
    print(" 2. VECTOR CLOCKS: CAUSAL TRACKING WITHOUT PHYSICAL CLOCKS")
    print("======================================================================")

    # Initial state
    v0 = VectorClock()
    print("Initial Vector Clock:", v0)

    # Client A mutates state on Node 1
    vA = v0.clone()
    vA.increment("node1")
    print("Client A writes on Node 1 ──> Vector Clock:", vA)

    # Scenario 1: Client B reads A's write, then writes on Node 2 (Causal Progression)
    vB_causal = vA.clone()
    vB_causal.increment("node2")
    print("Client B reads A and updates on Node 2 ──> Vector Clock:", vB_causal)
    print("Does B dominate A?", vB_causal.dominates(vA))
    print("Conflict status: NO CONFLICT (B causally succeeded A)")

    # Scenario 2: Concurrent write during network partition (Both start from vA)
    # Concurrent write on Node 1
    v_concurrent_1 = vA.clone()
    v_concurrent_1.increment("node1")  # [('node1', 2)]

    # Concurrent write on Node 2 (without having seen Node 1's second write)
    v_concurrent_2 = vA.clone()
    v_concurrent_2.increment("node2")  # [('node1', 1), ('node2', 1)]

    print(f"\nPartition Scenario:")
    print("Node 1 Branch:", v_concurrent_1)
    print("Node 2 Branch:", v_concurrent_2)
    is_conflicting = v_concurrent_1.is_concurrent(v_concurrent_2)
    print(f"Are mutations concurrent? {is_conflicting}")
    print("Result: Vector clock mathematically detects concurrent conflict!")
    print("Database presents both versions (siblings) to application for clean reconciliation.")

if __name__ == "__main__":
    run_simulation()
