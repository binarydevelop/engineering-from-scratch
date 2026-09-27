#!/usr/bin/env python3
"""
pipelines/idempotent_upsert.py
Demonstrates the critical difference between Naive Append and Idempotent Merge/Upsert.
Proves why idempotency is mandatory for reliable data pipelines.
"""
import duckdb
from pathlib import Path

def demonstrate_idempotency():
    con = duckdb.connect(":memory:")

    # Scenario A: The Naive Pipeline (Append Only)
    con.execute("""
        CREATE TABLE orders_naive (
            order_id VARCHAR,
            amount NUMERIC(10,2)
        );
    """)

    incoming_batch = [
        ("ord_001", 100.0),
        ("ord_002", 250.0)
    ]

    # Run 1
    con.executemany("INSERT INTO orders_naive VALUES (?, ?);", incoming_batch)
    count_run1 = con.execute("SELECT COUNT(*) FROM orders_naive;").fetchone()[0]

    # Run 2 (Simulating network timeout or scheduler retry)
    con.executemany("INSERT INTO orders_naive VALUES (?, ?);", incoming_batch)
    count_run2 = con.execute("SELECT COUNT(*) FROM orders_naive;").fetchone()[0]

    print("--- Scenario A: Naive Pipeline (Non-Idempotent) ---")
    print(f"  Count after Run 1: {count_run1} rows (Expected 2)")
    print(f"  Count after Run 2: {count_run2} rows (SILENT DUPLICATION! Failure!)")

    # Scenario B: The Idempotent Upsert Pipeline
    con.execute("""
        CREATE TABLE orders_idempotent (
            order_id VARCHAR PRIMARY KEY,
            amount NUMERIC(10,2)
        );
    """)

    def run_idempotent_batch(records):
        con.execute("CREATE TEMP TABLE stage_in (order_id VARCHAR, amount NUMERIC(10,2));")
        con.executemany("INSERT INTO stage_in VALUES (?, ?);", records)

        # Merge / Upsert: Delete matching keys, then insert
        con.execute("""
            DELETE FROM orders_idempotent
            WHERE order_id IN (SELECT order_id FROM stage_in);
        """)
        con.execute("""
            INSERT INTO orders_idempotent
            SELECT order_id, amount FROM stage_in;
        """)
        con.execute("DROP TABLE stage_in;")

    # Run 1
    run_idempotent_batch(incoming_batch)
    idem_count_run1 = con.execute("SELECT COUNT(*) FROM orders_idempotent;").fetchone()[0]

    # Run 2 (Exact duplicate rerun)
    run_idempotent_batch(incoming_batch)
    idem_count_run2 = con.execute("SELECT COUNT(*) FROM orders_idempotent;").fetchone()[0]

    print("\n--- Scenario B: Idempotent Pipeline ---")
    print(f"  Count after Run 1: {idem_count_run1} rows (Expected 2)")
    print(f"  Count after Run 2: {idem_count_run2} rows (IDENTICAL! Mathematically Idempotent!)")

    assert count_run2 == 4, "Naive pipeline should produce duplicate rows"
    assert idem_count_run2 == 2, "Idempotent pipeline must produce exactly 2 rows"
    print("\nAssertion Verified: Idempotent architecture prevents duplicate financial metrics.")
    con.close()

if __name__ == "__main__":
    demonstrate_idempotency()
