#!/usr/bin/env python3
"""
benchmarks/benchmark_small_files_compaction.py
Demonstrates the 'Small Files Problem' and the necessity of Compaction.
Measures file open / metadata overhead of 200 tiny Parquet files vs 1 compacted file.
"""
import os
import time
import duckdb
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent.parent / "outputs" / "benchmarks"
SMALL_FILES_DIR = BENCH_DIR / "small_files"
COMPACTED_FILE = BENCH_DIR / "compacted_file.parquet"

SMALL_FILES_DIR.mkdir(parents=True, exist_ok=True)

def setup_small_files(num_files=100, rows_per_file=500):
    print(f"Creating {num_files} tiny Parquet files ({rows_per_file} rows each)...")
    con = duckdb.connect()
    for i in range(num_files):
        con.execute(f"""
            COPY (
                SELECT range AS id, 'payload_' || range AS val
                FROM range({rows_per_file})
            ) TO '{SMALL_FILES_DIR}/part_{i:04d}.parquet' (FORMAT PARQUET);
        """)

    print("Compacting small files into single Parquet file...")
    t0 = time.perf_counter()
    con.execute(f"""
        COPY (
            SELECT * FROM read_parquet('{SMALL_FILES_DIR}/*.parquet')
        ) TO '{COMPACTED_FILE}' (FORMAT PARQUET);
    """)
    compaction_time = time.perf_counter() - t0
    print(f"Compaction completed in {compaction_time*1000:.2f} ms.")
    con.close()

def run_benchmark():
    con = duckdb.connect()

    print("\n" + "=" * 65)
    print("   BENCHMARK RESULT: SMALL FILES OVERHEAD VS COMPACTED FILE")
    print("=" * 65)

    # Test 1: Query 100 tiny files
    t0 = time.perf_counter()
    con.execute(f"SELECT count(*), max(id) FROM read_parquet('{SMALL_FILES_DIR}/*.parquet');").fetchall()
    small_files_time = time.perf_counter() - t0

    # Test 2: Query 1 compacted file
    t0 = time.perf_counter()
    con.execute(f"SELECT count(*), max(id) FROM read_parquet('{COMPACTED_FILE}');").fetchall()
    compacted_time = time.perf_counter() - t0

    print(f"  Scan 100 Small Files (File open & metadata penalty): {small_files_time * 1000:.2f} ms")
    print(f"  Scan 1 Compacted File (Single vectorized scan):     {compacted_time * 1000:.2f} ms")
    speedup = small_files_time / max(compacted_time, 0.0001)
    print(f"  Compaction Scan Speedup:                           {speedup:.1f}x faster!")
    print("=" * 65)
    con.close()

if __name__ == "__main__":
    setup_small_files(100, 500)
    run_benchmark()
