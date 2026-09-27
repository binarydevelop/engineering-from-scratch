#!/usr/bin/env python3
"""
benchmarks/benchmark_csv_vs_parquet.py
Empirical performance comparison: CSV vs Apache Parquet.
Measures:
1. On-disk storage footprint (bytes)
2. Full scan read latency
3. Single-column scan latency (Column Pruning proof)
4. Filtered aggregation latency
"""
import os
import time
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent.parent / "outputs" / "benchmarks"
BENCH_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = BENCH_DIR / "large_dataset.csv"
PARQUET_FILE = BENCH_DIR / "large_dataset.parquet"

def generate_benchmark_data(num_rows=200_000):
    print(f"Generating synthetic benchmark dataset ({num_rows:,} rows x 10 columns)...")
    con = duckdb.connect()
    con.execute(f"""
        CREATE TABLE bench_data AS
        SELECT
            range AS id,
            'user_' || (range % 5000)::VARCHAR AS user_id,
            CASE WHEN range % 3 = 0 THEN 'ELECTRONICS' WHEN range % 3 = 1 THEN 'APPAREL' ELSE 'BOOKS' END AS category,
            (random() * 500)::NUMERIC(10,2) AS amount,
            (random() * 40)::NUMERIC(10,2) AS tax,
            (random() * 540)::NUMERIC(10,2) AS total,
            'status_' || (range % 4)::VARCHAR AS status,
            'device_' || (range % 6)::VARCHAR AS device,
            'session_' || (range % 20000)::VARCHAR AS session_id,
            TIMESTAMP '2026-09-01 00:00:00' + INTERVAL (range % 86400) SECOND AS event_time
        FROM range({num_rows});
    """)

    # Export to CSV
    t0 = time.perf_counter()
    con.execute(f"COPY bench_data TO '{CSV_FILE}' (HEADER, DELIMITER ',');")
    csv_write_time = time.perf_counter() - t0

    # Export to Parquet (Snappy compression)
    t0 = time.perf_counter()
    con.execute(f"COPY bench_data TO '{PARQUET_FILE}' (FORMAT PARQUET, COMPRESSION 'SNAPPY');")
    parquet_write_time = time.perf_counter() - t0

    con.close()
    return csv_write_time, parquet_write_time

def run_benchmarks():
    csv_size = os.path.getsize(CSV_FILE)
    parquet_size = os.path.getsize(PARQUET_FILE)
    compression_ratio = (1 - (parquet_size / csv_size)) * 100

    print("\n" + "=" * 65)
    print("   BENCHMARK RESULT: CSV vs APACHE PARQUET")
    print("=" * 65)
    print(f"  CSV File Size:       {csv_size / 1024 / 1024:.2f} MB")
    print(f"  Parquet File Size:   {parquet_size / 1024 / 1024:.2f} MB")
    print(f"  Storage Reduction:   {compression_ratio:.1f}% less disk space!")
    print("-" * 65)

    con = duckdb.connect()

    # Test 1: Full table scan & count
    t0 = time.perf_counter()
    con.execute(f"SELECT count(*) FROM read_csv_auto('{CSV_FILE}');").fetchall()
    csv_scan_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    con.execute(f"SELECT count(*) FROM read_parquet('{PARQUET_FILE}');").fetchall()
    parquet_scan_time = time.perf_counter() - t0

    print(f"  Full Scan Count:")
    print(f"    CSV:     {csv_scan_time * 1000:.2f} ms")
    print(f"    Parquet: {parquet_scan_time * 1000:.2f} ms ({csv_scan_time / max(parquet_scan_time, 0.0001):.1f}x faster)")

    # Test 2: Single Column Aggregation (Column Pruning)
    t0 = time.perf_counter()
    con.execute(f"SELECT sum(total) FROM read_csv_auto('{CSV_FILE}');").fetchall()
    csv_agg_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    con.execute(f"SELECT sum(total) FROM read_parquet('{PARQUET_FILE}');").fetchall()
    parquet_agg_time = time.perf_counter() - t0

    print(f"\n  Column Pruning (SELECT SUM(total)):")
    print(f"    CSV (reads all 10 cols):     {csv_agg_time * 1000:.2f} ms")
    print(f"    Parquet (reads 1 col only):  {parquet_agg_time * 1000:.2f} ms ({csv_agg_time / max(parquet_agg_time, 0.0001):.1f}x faster)")

    # Test 3: Filtered Scan
    t0 = time.perf_counter()
    con.execute(f"SELECT category, sum(total) FROM read_csv_auto('{CSV_FILE}') WHERE category = 'ELECTRONICS' GROUP BY category;").fetchall()
    csv_filt_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    con.execute(f"SELECT category, sum(total) FROM read_parquet('{PARQUET_FILE}') WHERE category = 'ELECTRONICS' GROUP BY category;").fetchall()
    parquet_filt_time = time.perf_counter() - t0

    print(f"\n  Filtered Query (WHERE category = 'ELECTRONICS'):")
    print(f"    CSV:     {csv_filt_time * 1000:.2f} ms")
    print(f"    Parquet: {parquet_filt_time * 1000:.2f} ms ({csv_filt_time / max(parquet_filt_time, 0.0001):.1f}x faster)")
    print("=" * 65)

    con.close()

if __name__ == "__main__":
    generate_benchmark_data(100_000)
    run_benchmarks()
