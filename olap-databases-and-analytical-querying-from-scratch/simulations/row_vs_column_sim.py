#!/usr/bin/env python3
"""
Simulation: Row-Oriented vs Column-Oriented Storage from First Principles.

Demonstrates:
  1. Memory layout of Row Store (Array of Structs / Tuples) vs Column Store (Struct of Arrays)
  2. Byte count physically traversed during an analytical aggregation
  3. CPU cache effects and wall-clock execution time
"""

import sys
import time
import random
from typing import List, Dict, Any
from tabulate import tabulate

def create_synthetic_data(n_rows: int):
    countries = ["US", "DE", "UK", "JP", "FR", "IN"]
    devices = ["mobile_ios", "mobile_android", "desktop"]
    
    # 1. Row store representation: List of dicts/tuples
    row_store = []
    
    # 2. Column store representation: Dict of flat lists
    col_store = {
        "event_id": [],
        "user_id": [],
        "country": [],
        "device": [],
        "created_at_epoch": [],
        "revenue": [],
        "duration_ms": [],
        "is_converted": []
    }
    
    for i in range(n_rows):
        eid = i + 1000000
        uid = (i * 37) % 50000 + 100000
        country = countries[i % len(countries)]
        device = devices[i % len(devices)]
        ts = 1700000000 + (i % 86400)
        rev = round(10.0 + (i % 500) * 1.25, 2)
        dur = (i % 1000) + 50
        conv = (i % 20) == 0
        
        # Append to row store
        row_store.append((eid, uid, country, device, ts, rev, dur, conv))
        
        # Append to column store
        col_store["event_id"].append(eid)
        col_store["user_id"].append(uid)
        col_store["country"].append(country)
        col_store["device"].append(device)
        col_store["created_at_epoch"].append(ts)
        col_store["revenue"].append(rev)
        col_store["duration_ms"].append(dur)
        col_store["is_converted"].append(conv)
        
    return row_store, col_store

def query_row_store(row_store: List[tuple]):
    """
    Query: SELECT country, SUM(revenue) FROM table GROUP BY country
    Notice: Every row tuple must be dereferenced, pulling all 8 fields into CPU registers.
    """
    totals = {}
    bytes_inspected = 0
    t0 = time.perf_counter()
    
    for row in row_store:
        # Tuple layout: (eid, uid, country, device, ts, rev, dur, conv)
        country = row[2]
        revenue = row[5]
        totals[country] = totals.get(country, 0.0) + revenue
        # Full row size: 8 ints/floats/pointers ~ 64 bytes minimum
        bytes_inspected += 64
        
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return totals, elapsed_ms, bytes_inspected

def query_col_store(col_store: Dict[str, list]):
    """
    Query: SELECT country, SUM(revenue) FROM table GROUP BY country
    Notice: ONLY the 'country' and 'revenue' arrays are touched.
    The remaining 6 columns (event_id, user_id, device, ts, dur, conv) are NEVER read.
    """
    totals = {}
    bytes_inspected = 0
    t0 = time.perf_counter()
    
    country_arr = col_store["country"]
    revenue_arr = col_store["revenue"]
    n = len(country_arr)
    
    for i in range(n):
        country = country_arr[i]
        revenue = revenue_arr[i]
        totals[country] = totals.get(country, 0.0) + revenue
        # Touched: 1 pointer/ref for country (8 bytes) + 1 float for revenue (8 bytes) = 16 bytes
        bytes_inspected += 16
        
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return totals, elapsed_ms, bytes_inspected

def main():
    n_rows = 1_000_000
    print("\n" + "="*70)
    print(f"  SIMULATION: Row Store vs Column Store ({n_rows:,} records)")
    print("="*70)
    print(f"[*] Allocating synthetic records in memory...")
    row_store, col_store = create_synthetic_data(n_rows)
    
    print(f"[*] Executing Analytical Query: SELECT country, SUM(revenue) GROUP BY country\n")
    
    # Run Row Store Query
    res_row, time_row, bytes_row = query_row_store(row_store)
    
    # Run Column Store Query
    res_col, time_col, bytes_col = query_col_store(col_store)
    
    # Assert correctness
    for k in res_row:
        assert abs(res_row[k] - res_col[k]) < 0.01, f"Mismatch on {k}"
        
    table_data = [
        ["Row Store (Array of Structs)", f"{bytes_row / (1024*1024):.1f} MB", f"{time_row:.2f} ms", "1.00x (Baseline)"],
        ["Column Store (Struct of Arrays)", f"{bytes_col / (1024*1024):.1f} MB", f"{time_col:.2f} ms", f"{time_row / max(0.01, time_col):.2f}x faster"],
    ]
    
    print(tabulate(table_data, headers=["Storage Model", "Bytes Traversed", "Execution Latency", "Speedup"], tablefmt="github"))
    
    reduction = ((bytes_row - bytes_col) / bytes_row) * 100.0
    print(f"\n[✓] Column Projection avoided scanning {reduction:.1f}% of memory bytes!")
    print(f"[✓] Both engines returned identical aggregated measures across {len(res_row)} groups.\n")

if __name__ == "__main__":
    main()
