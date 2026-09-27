#!/usr/bin/env python3
"""
Simulation: Volcano Tuple-at-a-Time vs Vectorized Batch Execution.

Demonstrates:
  1. The Volcano Iterator pattern: next() calls returning 1 tuple.
  2. The Vectorized Execution pattern: process() calls handling a chunk (2,048 values).
  3. Function call overhead amortization and performance differential.
"""

import sys
import time
from typing import List, Optional, Tuple
from tabulate import tabulate

# -------------------------------------------------------------
# 1. VOLCANO ITERATOR MODEL (Tuple-at-a-Time)
# -------------------------------------------------------------
class VolcanoScan:
    def __init__(self, prices: List[float], discounts: List[float]):
        self.prices = prices
        self.discounts = discounts
        self.idx = 0
        self.n = len(prices)
        
    def next(self) -> Optional[Tuple[float, float]]:
        if self.idx >= self.n:
            return None
        val = (self.prices[self.idx], self.discounts[self.idx])
        self.idx += 1
        return val

class VolcanoFilter:
    def __init__(self, child: VolcanoScan, min_price: float):
        self.child = child
        self.min_price = min_price
        
    def next(self) -> Optional[Tuple[float, float]]:
        while True:
            tup = self.child.next()
            if tup is None:
                return None
            if tup[0] >= self.min_price:
                return tup

class VolcanoProjectAggregate:
    def __init__(self, child: VolcanoFilter):
        self.child = child
        
    def execute(self) -> Tuple[int, float, int]:
        count = 0
        total_revenue = 0.0
        dispatch_calls = 0
        while True:
            dispatch_calls += 1
            tup = self.child.next()
            if tup is None:
                break
            count += 1
            # price - discount
            total_revenue += (tup[0] - tup[1])
        return count, total_revenue, dispatch_calls

# -------------------------------------------------------------
# 2. VECTORIZED EXECUTION MODEL (Batch / DataChunk)
# -------------------------------------------------------------
VECTOR_SIZE = 2048

class VectorScan:
    def __init__(self, prices: List[float], discounts: List[float]):
        self.prices = prices
        self.discounts = discounts
        self.offset = 0
        self.n = len(prices)
        
    def next_chunk(self) -> Optional[Tuple[List[float], List[float]]]:
        if self.offset >= self.n:
            return None
        end = min(self.offset + VECTOR_SIZE, self.n)
        chunk = (self.prices[self.offset:end], self.discounts[self.offset:end])
        self.offset = end
        return chunk

class VectorizedEngine:
    def __init__(self, scanner: VectorScan, min_price: float):
        self.scanner = scanner
        self.min_price = min_price
        
    def execute(self) -> Tuple[int, float, int]:
        total_count = 0
        total_revenue = 0.0
        dispatch_calls = 0
        
        while True:
            dispatch_calls += 1
            chunk = self.scanner.next_chunk()
            if chunk is None:
                break
                
            prices, discounts = chunk
            # Tight, branch-predictable array vector loop
            chunk_len = len(prices)
            for i in range(chunk_len):
                p = prices[i]
                if p >= self.min_price:
                    total_count += 1
                    total_revenue += (p - discounts[i])
                    
        return total_count, total_revenue, dispatch_calls

def main():
    n = 2_000_000
    min_price = 100.0
    print("\n" + "="*70)
    print(f"  SIMULATION: Volcano Tuple-at-a-Time vs Vectorized Execution ({n:,} rows)")
    print(f"  Vector Size: {VECTOR_SIZE} values per chunk | Predicate: price >= {min_price}")
    print("="*70)
    
    # Generate synthetic arrays
    prices = [float(50.0 + (i % 200) * 1.5) for i in range(n)]
    discounts = [float((i % 10) * 1.25) for i in range(n)]
    
    # 1. Run Volcano
    print("[*] Running Volcano Iterator Model (Single-tuple next() dispatch)...")
    v_scan = VolcanoScan(prices, discounts)
    v_filter = VolcanoFilter(v_scan, min_price)
    v_agg = VolcanoProjectAggregate(v_filter)
    
    t0 = time.perf_counter()
    cnt_v, rev_v, calls_v = v_agg.execute()
    time_volcano_ms = (time.perf_counter() - t0) * 1000.0
    
    # 2. Run Vectorized
    print("[*] Running Vectorized Engine (2,048 values per batch)...")
    vec_scan = VectorScan(prices, discounts)
    vec_engine = VectorizedEngine(vec_scan, min_price)
    
    t0 = time.perf_counter()
    cnt_vec, rev_vec, calls_vec = vec_engine.execute()
    time_vec_ms = (time.perf_counter() - t0) * 1000.0
    
    assert cnt_v == cnt_vec, "Row count mismatch"
    assert abs(rev_v - rev_vec) < 0.01, "Revenue mismatch"
    
    table = [
        ["Volcano Iterator (Tuple-at-a-Time)", f"{calls_v:,}", f"{time_volcano_ms:.2f} ms", "1.00x (Baseline)"],
        ["Vectorized Batch (2048 values/chunk)", f"{calls_vec:,}", f"{time_vec_ms:.2f} ms", f"{time_volcano_ms / max(0.01, time_vec_ms):.2f}x faster"],
    ]
    
    print("\n" + tabulate(table, headers=["Execution Model", "Function Dispatches", "Latency (ms)", "Speedup"], tablefmt="github"))
    
    call_reduction = ((calls_v - calls_vec) / calls_v) * 100.0
    print(f"\n[✓] Vectorized execution eliminated {call_reduction:.2f}% of function dispatch overhead!")
    print(f"[✓] Both models computed matching results: {cnt_vec:,} rows, ${rev_vec:,.2f} net revenue.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
