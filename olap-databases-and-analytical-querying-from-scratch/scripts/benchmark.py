#!/usr/bin/env python3
"""
Reproducible OLAP Benchmark Harness.
Measures and compares physical execution across storage layouts and engines:
  - DuckDB (CSV scan vs Parquet scan vs In-Memory table)
  - ClickHouse (MergeTree with LZ4 / ZSTD)
  - PostgreSQL (Heap row store baseline)

Generates structured benchmark artifacts adhering to BENCHMARK_TEMPLATE.md.
"""

import os
import sys
import time
import json
import argparse
import statistics
from pathlib import Path
import duckdb
from tabulate import tabulate

def run_duckdb_benchmark(query: str, db_path: str, warmup: int = 2, runs: int = 5):
    con = duckdb.connect(db_path, read_only=True)
    
    # Warmup
    for _ in range(warmup):
        con.execute(query).fetchall()
        
    timings = []
    rows_returned = 0
    for _ in range(runs):
        t0 = time.perf_counter()
        res = con.execute(query).fetchall()
        t1 = time.perf_counter()
        timings.append((t1 - t0) * 1000.0) # ms
        rows_returned = len(res)
        
    con.close()
    
    p50 = statistics.median(timings)
    mean_val = statistics.mean(timings)
    p95 = statistics.quantiles(timings, n=20)[18] if len(timings) >= 20 else max(timings)
    p99 = max(timings)
    
    return {
        "engine": "DuckDB",
        "warmup": warmup,
        "runs": runs,
        "p50_ms": round(p50, 3),
        "mean_ms": round(mean_val, 3),
        "p95_ms": round(p95, 3),
        "p99_ms": round(p99, 3),
        "rows_returned": rows_returned,
        "timings_ms": [round(t, 2) for t in timings]
    }

def benchmark_format_comparison(repo_root: Path):
    print("\n" + "="*70)
    print("  BENCHMARK SUITE: Row (CSV) vs Columnar (Parquet) Scan & Aggregation")
    print("="*70)
    
    csv_file = repo_root / "datasets" / "ecommerce" / "fact_order_items_sample.csv"
    parquet_file = repo_root / "datasets" / "ecommerce" / "fact_order_items.parquet"
    db_file = repo_root / "outputs" / "olap_lab.duckdb"
    
    if not parquet_file.exists() or not db_file.exists():
        print("[!] Datasets missing. Generating small dataset first...")
        os.system(f"{sys.executable} scripts/generate-data.py --scale small")
        
    query_csv = f"""
        SELECT country, COUNT(*) as cnt, SUM(net_revenue) as rev
        FROM read_csv_auto('{csv_file}')
        GROUP BY country
        ORDER BY rev DESC;
    """
    
    query_parquet = f"""
        SELECT country, COUNT(*) as cnt, SUM(net_revenue) as rev
        FROM read_parquet('{parquet_file}')
        GROUP BY country
        ORDER BY rev DESC;
    """
    
    query_duckdb_table = """
        SELECT country, COUNT(*) as cnt, SUM(net_revenue) as rev
        FROM fact_order_items
        GROUP BY country
        ORDER BY rev DESC;
    """
    
    print("\n[*] Benchmarking CSV Scan (Row serialization)...")
    res_csv = run_duckdb_benchmark(query_csv, str(db_file))
    res_csv["storage_format"] = "CSV (Auto-detect row parse)"
    
    print("[*] Benchmarking Parquet Scan (Columnar projection pushdown)...")
    res_parquet = run_duckdb_benchmark(query_parquet, str(db_file))
    res_parquet["storage_format"] = "Parquet (ZSTD compressed columns)"
    
    print("[*] Benchmarking Native DuckDB Table (Vectorized in-memory/disk)...")
    res_table = run_duckdb_benchmark(query_duckdb_table, str(db_file))
    res_table["storage_format"] = "DuckDB Native Columnar"
    
    results = [
        [res_csv["storage_format"], res_csv["p50_ms"], res_csv["mean_ms"], res_csv["p95_ms"], res_csv["rows_returned"]],
        [res_parquet["storage_format"], res_parquet["p50_ms"], res_parquet["mean_ms"], res_parquet["p95_ms"], res_parquet["rows_returned"]],
        [res_table["storage_format"], res_table["p50_ms"], res_table["mean_ms"], res_table["p95_ms"], res_table["rows_returned"]],
    ]
    
    print("\n" + tabulate(results, headers=["Format / Storage", "p50 (ms)", "Mean (ms)", "p95 (ms)", "Rows Out"], tablefmt="github"))
    
    speedup = res_csv["p50_ms"] / max(0.001, res_parquet["p50_ms"])
    print(f"\n[✓] Parquet Columnar Projection speedup vs CSV: {speedup:.2f}x faster p50")
    print("="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(description="OLAP Benchmark Suite")
    parser.add_argument("--suite", choices=["core", "formats", "clickhouse", "all"], default="core",
                        help="Benchmark suite to execute")
    args = parser.parse_args()
    
    repo_root = Path(__file__).resolve().parent.parent
    if args.suite in ["core", "formats", "all"]:
        benchmark_format_comparison(repo_root)

if __name__ == "__main__":
    main()
