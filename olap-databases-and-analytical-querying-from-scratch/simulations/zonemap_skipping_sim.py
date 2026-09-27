#!/usr/bin/env python3
"""
Simulation: Zone Maps & Data Skipping from First Principles.

Demonstrates:
  1. Block-level Min/Max metadata (Zone Maps)
  2. How data ordering (Sort Key) radically alters data skipping efficacy
  3. Physical block I/O comparison: Full Scan vs Random Order vs Sorted Order
"""

import sys
import time
import random
from typing import List, Tuple
from tabulate import tabulate

BLOCK_SIZE = 8192 # Like ClickHouse granules (8,192 rows)

class Block:
    def __init__(self, block_id: int, timestamps: List[int], values: List[float]):
        self.block_id = block_id
        self.timestamps = timestamps
        self.values = values
        # Zone map metadata:
        self.min_ts = min(timestamps)
        self.max_ts = max(timestamps)
        
    def matches_predicate(self, lower_ts: int, upper_ts: int) -> bool:
        # Zone map rejection test
        if self.max_ts < lower_ts or self.min_ts > upper_ts:
            return False # Block guaranteed to contain NO matching rows!
        return True

def build_blocks(timestamps: List[int], values: List[float]) -> List[Block]:
    blocks = []
    n = len(timestamps)
    for b_idx, i in enumerate(range(0, n, BLOCK_SIZE)):
        end = min(i + BLOCK_SIZE, n)
        blocks.append(Block(b_idx, timestamps[i:end], values[i:end]))
    return blocks

def execute_query(blocks: List[Block], lower_ts: int, upper_ts: int) -> Tuple[int, float, int, int]:
    """
    Query: SELECT COUNT(*), SUM(value) WHERE timestamp BETWEEN lower_ts AND upper_ts
    """
    total_count = 0
    total_sum = 0.0
    blocks_scanned = 0
    blocks_skipped = 0
    
    for b in blocks:
        if not b.matches_predicate(lower_ts, upper_ts):
            blocks_skipped += 1
            continue # Data skipping: bypass reading column arrays!
            
        blocks_scanned += 1
        for ts, v in zip(b.timestamps, b.values):
            if lower_ts <= ts <= upper_ts:
                total_count += 1
                total_sum += v
                
    return total_count, total_sum, blocks_scanned, blocks_skipped

def main():
    n_rows = 1_000_000
    print("\n" + "="*70)
    print(f"  SIMULATION: Zone Map Data Skipping & Sort Key Impact ({n_rows:,} rows)")
    print(f"  Granule / Block Size: {BLOCK_SIZE:,} rows | Total Blocks: {n_rows // BLOCK_SIZE + 1}")
    print("="*70)
    
    # Base timestamp range: 30 days
    base_ts = 1700000000
    ts_range = 30 * 86400
    
    # 1. Unsorted (Random) Order
    random_ts = [base_ts + random.randint(0, ts_range) for _ in range(n_rows)]
    values = [round(10.0 + (i % 100) * 0.5, 2) for i in range(n_rows)]
    unsorted_blocks = build_blocks(random_ts, values)
    
    # 2. Sorted Order (ORDER BY timestamp)
    sorted_ts = sorted(random_ts)
    sorted_blocks = build_blocks(sorted_ts, values)
    
    # Selective Predicate: Query for a 2-day window (2 days out of 30 days = 6.6% selectivity)
    query_start = base_ts + (10 * 86400)
    query_end = base_ts + (12 * 86400)
    
    print(f"[*] Query Predicate: WHERE timestamp BETWEEN Day 10 AND Day 12 (6.6% selectivity)")
    
    # Run Unsorted
    t0 = time.perf_counter()
    cnt_u, sum_u, scan_u, skip_u = execute_query(unsorted_blocks, query_start, query_end)
    time_u_ms = (time.perf_counter() - t0) * 1000.0
    
    # Run Sorted
    t0 = time.perf_counter()
    cnt_s, sum_s, scan_s, skip_s = execute_query(sorted_blocks, query_start, query_end)
    time_s_ms = (time.perf_counter() - t0) * 1000.0
    
    assert cnt_u == cnt_s, "Result count mismatch"
    
    table = [
        ["Random / Unsorted Order", f"{scan_u} / {len(unsorted_blocks)}", f"{skip_u} ({(skip_u/len(unsorted_blocks))*100:.1f}%)", f"{time_u_ms:.2f} ms", "1.00x"],
        ["Sorted Order (ORDER BY ts)", f"{scan_s} / {len(sorted_blocks)}", f"{skip_s} ({(skip_s/len(sorted_blocks))*100:.1f}%)", f"{time_s_ms:.2f} ms", f"{time_u_ms / max(0.01, time_s_ms):.2f}x faster"],
    ]
    
    print("\n" + tabulate(table, headers=["Data Layout", "Blocks Scanned", "Blocks Skipped", "Latency (ms)", "Speedup"], tablefmt="github"))
    
    print(f"\n[✓] Sorted layout allowed Zone Maps to skip {skip_s} out of {len(sorted_blocks)} blocks ({(skip_s/len(sorted_blocks))*100:.1f}%)!")
    print(f"[✓] Unsorted layout suffered 0% skipping because every block's min/max overlapped the query window.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
