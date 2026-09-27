#!/usr/bin/env python3
"""
benchmarks/benchmark_partition_pruning.py
Demonstrates the power of Partition Pruning.
Compares querying a single unpartitioned table vs partitioned directory layout.
"""
import time
import duckdb
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent.parent / "outputs" / "benchmarks"
BENCH_DIR.mkdir(parents=True, exist_ok=True)

UNPARTITIONED_FILE = BENCH_DIR / "unpartitioned_events.parquet"
PARTITIONED_DIR = BENCH_DIR / "partitioned_events"

def setup_partition_benchmark():
    con = duckdb.connect()
    # Generate 10 days of event data, 20,000 rows per day = 200,000 rows
    print("Generating partition pruning dataset (200,000 rows across 10 days)...")
    con.execute("""
        CREATE TABLE events AS
        SELECT
            range AS event_id,
            (TIMESTAMP '2026-09-01' + INTERVAL (range % 10) DAY)::DATE AS event_date,
            'user_' || (range % 1000)::VARCHAR AS user_id,
            (random() * 100)::NUMERIC(10,2) AS value
        FROM range(200000);
    """)

    # Export unpartitioned
    con.execute(f"COPY events TO '{UNPARTITIONED_FILE}' (FORMAT PARQUET);")

    # Export partitioned by event_date
    con.execute(f"COPY events TO '{PARTITIONED_DIR}' (FORMAT PARQUET, PARTITION_BY (event_date), OVERWRITE_OR_IGNORE 1);")
    con.close()

def run_benchmark():
    con = duckdb.connect()
    target_date = "2026-09-05"

    print("\n" + "=" * 65)
    print("   BENCHMARK RESULT: PARTITION PRUNING (Query 1 single day)")
    print("=" * 65)

    # Test 1: Scan Unpartitioned File (Must scan entire file and evaluate predicate)
    t0 = time.perf_counter()
    con.execute(f"SELECT sum(value) FROM read_parquet('{UNPARTITIONED_FILE}') WHERE event_date = '{target_date}';").fetchall()
    unpart_time = time.perf_counter() - t0

    # Test 2: Scan Partitioned Directory (Engine skips other 9 partitions entirely)
    t0 = time.perf_counter()
    con.execute(f"SELECT sum(value) FROM read_parquet('{PARTITIONED_DIR}/*/*.parquet', hive_partitioning=1) WHERE event_date = '{target_date}';").fetchall()
    part_time = time.perf_counter() - t0

    print(f"  Unpartitioned Scan (scans all 10 days): {unpart_time * 1000:.2f} ms")
    print(f"  Partitioned Scan (pruned 90% of files):  {part_time * 1000:.2f} ms")
    speedup = unpart_time / max(part_time, 0.0001)
    print(f"  Partition Pruning Speedup:              {speedup:.1f}x faster!")
    print("=" * 65)
    con.close()

if __name__ == "__main__":
    setup_partition_benchmark()
    run_benchmark()
