#!/usr/bin/env python3
"""
Simulation: HyperLogLog Cardinality Estimation from First Principles.

Demonstrates:
  1. HLL register array (m = 2^p buckets)
  2. 64-bit hashing and leading zero counting: rho(w)
  3. Harmonic mean calculation and bias correction
  4. Memory footprint vs Exact Set (COUNT(DISTINCT))
"""

import sys
import time
import math
import hashlib
from typing import List
from tabulate import tabulate

class HyperLogLog:
    def __init__(self, precision_p: int = 12):
        self.p = precision_p
        self.m = 1 << precision_p # 2^p registers (e.g. 2^12 = 4,096 registers)
        self.registers = [0] * self.m
        
        # Alpha constant calculation
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1.0 + 1.079 / self.m)
            
    def _hash(self, value: str) -> int:
        h = hashlib.sha256(value.encode("utf-8")).digest()
        return int.from_bytes(h[:8], "little")
        
    def _clz(self, x: int) -> int:
        # Count leading zeros in binary representation (up to 64 - p bits)
        if x == 0:
            return 64 - self.p
        bits = 64 - self.p
        count = 0
        while (x & (1 << (bits - 1))) == 0 and bits > 0:
            count += 1
            bits -= 1
        return count + 1

    def add(self, value: str):
        x = self._hash(value)
        # First p bits determine register index
        j = x >> (64 - self.p)
        # Remaining bits used for leading zero run
        w = x & ((1 << (64 - self.p)) - 1)
        rho = self._clz(w)
        if rho > self.registers[j]:
            self.registers[j] = rho

    def estimate(self) -> float:
        # Indicator: sum of 2^(-M[j])
        z = sum(2.0 ** (-reg) for reg in self.registers)
        raw_est = self.alpha * (self.m ** 2) / z
        
        # Small range correction (Linear counting)
        if raw_est <= 2.5 * self.m:
            zeros = self.registers.count(0)
            if zeros != 0:
                return self.m * math.log(self.m / zeros)
        return raw_est

def main():
    n_distinct = 500_000
    precision = 12 # 4,096 bytes
    print("\n" + "="*70)
    print(f"  SIMULATION: HyperLogLog vs Exact Set ({n_distinct:,} distinct elements)")
    print(f"  HLL Precision p={precision} (m={1<<precision} registers, 4 KB memory)")
    print("="*70)
    
    # 1. Exact Set (Python set storing 500k strings)
    print("[*] Computing Exact Set (COUNT(DISTINCT))...")
    exact_set = set()
    t0 = time.perf_counter()
    for i in range(n_distinct):
        exact_set.add(f"user_id_{i}")
    time_exact = (time.perf_counter() - t0) * 1000.0
    mem_exact_bytes = sys.getsizeof(exact_set) + sum(sys.getsizeof(s) for s in list(exact_set)[:1000]) * (n_distinct // 1000)
    
    # 2. HyperLogLog
    print("[*] Computing HyperLogLog Sketch...")
    hll = HyperLogLog(precision_p=precision)
    t0 = time.perf_counter()
    for i in range(n_distinct):
        hll.add(f"user_id_{i}")
    time_hll = (time.perf_counter() - t0) * 1000.0
    mem_hll_bytes = len(hll.registers) # 1 byte per register = 4,096 bytes
    
    est = hll.estimate()
    err_pct = abs(est - n_distinct) / n_distinct * 100.0
    
    table = [
        ["Exact Set (COUNT(DISTINCT))", f"{n_distinct:,}", f"{mem_exact_bytes / (1024*1024):.2f} MB", f"{time_exact:.2f} ms", "0.00% (Exact)"],
        ["HyperLogLog Sketch (p=12)", f"{int(est):,}", f"{mem_hll_bytes / 1024:.2f} KB", f"{time_hll:.2f} ms", f"{err_pct:.2f}% error"],
    ]
    
    print("\n" + tabulate(table, headers=["Method", "Distinct Count", "Memory Footprint", "Compute Time", "Accuracy"], tablefmt="github"))
    
    mem_reduction = ((mem_exact_bytes - mem_hll_bytes) / mem_exact_bytes) * 100.0
    print(f"\n[✓] HyperLogLog reduced memory consumption by {mem_reduction:.2f}% (from {mem_exact_bytes/(1024*1024):.1f} MB down to 4 KB)!")
    print(f"[✓] Standard theoretical error bound for p={precision}: ±{1.04 / math.sqrt(1<<precision) * 100:.2f}%. Measured: {err_pct:.2f}%.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
