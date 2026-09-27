#!/usr/bin/env python3
"""
Simulation: Distributed Aggregation & Network Shuffle from First Principles.

Demonstrates:
  1. Distributed Workers scanning local shards
  2. Local Partial Aggregation (Worker-level map phase)
  3. Network Shuffle: Naive Full Row Transfer vs Partial State Transfer
  4. Global Coordinator Merge (Reduce phase)
"""

import sys
import time
import hashlib
from typing import List, Dict, Tuple
from tabulate import tabulate

N_WORKERS = 4

class WorkerNode:
    def __init__(self, node_id: int, local_shard: List[Tuple[str, float]]):
        self.node_id = node_id
        self.local_shard = local_shard # [(category, revenue), ...]
        
    def execute_naive_scan(self) -> List[Tuple[str, float]]:
        # Naive: Ship every raw row to coordinator across network
        return list(self.local_shard)
        
    def execute_partial_aggregation(self) -> Dict[str, Tuple[int, float]]:
        # Partial aggregation: accumulate locally first
        local_state = {}
        for cat, rev in self.local_shard:
            if cat not in local_state:
                local_state[cat] = (0, 0.0)
            cnt, total = local_state[cat]
            local_state[cat] = (cnt + 1, total + rev)
        return local_state

def coordinator_merge_naive(shuffled_rows: List[Tuple[str, float]]) -> Dict[str, Tuple[int, float, float]]:
    global_state = {}
    for cat, rev in shuffled_rows:
        if cat not in global_state:
            global_state[cat] = [0, 0.0]
        global_state[cat][0] += 1
        global_state[cat][1] += rev
    return {k: (v[0], v[1], v[1]/v[0]) for k, v in global_state.items()}

def coordinator_merge_partial(worker_states: List[Dict[str, Tuple[int, float]]]) -> Dict[str, Tuple[int, float, float]]:
    global_state = {}
    for w_state in worker_states:
        for cat, (cnt, total) in w_state.items():
            if cat not in global_state:
                global_state[cat] = [0, 0.0]
            global_state[cat][0] += cnt
            global_state[cat][1] += total
    return {k: (v[0], v[1], v[1]/v[0]) for k, v in global_state.items()}

def main():
    total_rows = 1_000_000
    rows_per_worker = total_rows // N_WORKERS
    categories = ["Electronics", "Apparel", "Home", "Books", "Sports", "Beauty", "Automotive", "Garden"]
    
    print("\n" + "="*70)
    print(f"  SIMULATION: Distributed Aggregation & Network Shuffle ({total_rows:,} rows)")
    print(f"  Cluster Configuration: {N_WORKERS} Worker Nodes | Group Cardinality: {len(categories)}")
    print("="*70)
    
    # Generate shards for 4 workers
    workers = []
    for w_id in range(N_WORKERS):
        shard = []
        for i in range(rows_per_worker):
            cat = categories[(w_id * 17 + i) % len(categories)]
            rev = round(15.0 + (i % 250) * 1.5, 2)
            shard.append((cat, rev))
        workers.append(WorkerNode(w_id, shard))
        
    # Scenario A: Naive Distributed Query (Send all raw rows over network)
    print("\n[*] Running Scenario A: Naive Raw Row Shuffle (Ship all data to coordinator)...")
    t0 = time.perf_counter()
    all_raw_rows = []
    network_bytes_naive = 0
    for w in workers:
        rows = w.execute_naive_scan()
        all_raw_rows.extend(rows)
        # 1 string ref + 1 float64 = ~24 bytes per row serialized
        network_bytes_naive += len(rows) * 24
        
    final_res_a = coordinator_merge_naive(all_raw_rows)
    time_naive_ms = (time.perf_counter() - t0) * 1000.0
    
    # Scenario B: Partial Aggregation at Workers (Two-Phase Aggregate)
    print("[*] Running Scenario B: Worker Partial Aggregation (Ship only grouped states)...")
    t0 = time.perf_counter()
    partial_states = []
    network_bytes_partial = 0
    for w in workers:
        p_state = w.execute_partial_aggregation()
        partial_states.append(p_state)
        # Serialized state: category string (16 bytes) + count (8 bytes) + sum (8 bytes) = 32 bytes per group
        network_bytes_partial += len(p_state) * 32
        
    final_res_b = coordinator_merge_partial(partial_states)
    time_partial_ms = (time.perf_counter() - t0) * 1000.0
    
    # Verify exact match
    for k in final_res_a:
        assert final_res_a[k][0] == final_res_b[k][0], "Count mismatch"
        assert abs(final_res_a[k][1] - final_res_b[k][1]) < 0.01, "Sum mismatch"
        
    table = [
        ["Naive Row Shuffle", f"{network_bytes_naive / (1024*1024):.2f} MB", f"{total_rows:,} rows", f"{time_naive_ms:.2f} ms", "1.00x"],
        ["Worker Partial Aggregation", f"{network_bytes_partial / 1024:.2f} KB", f"{len(categories)*N_WORKERS} states", f"{time_partial_ms:.2f} ms", f"{time_naive_ms / max(0.01, time_partial_ms):.2f}x faster"],
    ]
    
    print("\n" + tabulate(table, headers=["Distributed Strategy", "Network Bytes Sent", "Payload Volume", "Compute Latency", "Speedup"], tablefmt="github"))
    
    net_reduction = ((network_bytes_naive - network_bytes_partial) / network_bytes_naive) * 100.0
    print(f"\n[✓] Two-Phase Partial Aggregation reduced network traffic by {net_reduction:.4f}% (from {network_bytes_naive/(1024*1024):.1f} MB down to {network_bytes_partial/1024:.2f} KB)!")
    print(f"[✓] Coordinator CPU load drastically decreased because it only merged {len(categories)*N_WORKERS} aggregate tuples instead of 1,000,000 raw rows.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
