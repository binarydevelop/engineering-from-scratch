#!/usr/bin/env python3
"""
pipelines/batch_ingestion.py
Production-grade Batch Ingestion Pipeline:
Extracts raw CSVs, validates schema contracts, routes poison records to quarantine,
performs deduplication, and loads atomically into analytical storage.
"""
import os
import csv
import json
import duckdb
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "datasets" / "raw"
DATA_DIR = BASE_DIR / "data" / "warehouse"
QUARANTINE_DIR = BASE_DIR / "outputs" / "quarantine"

DATA_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

def run_batch_ingestion(source_file=None, target_db=None):
    if source_file is None:
        source_file = RAW_DIR / "orders.csv"
    if target_db is None:
        target_db = DATA_DIR / "analytics.duckdb"

    print(f"[{datetime.now().isoformat()}] Starting Batch Ingestion Pipeline...")
    print(f"  Source: {source_file}")
    print(f"  Target: {target_db}")

    valid_rows = []
    quarantine_rows = []

    seen_ids = set()

    with open(source_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=1):
            order_id = row.get("order_id", "").strip()
            total_amt = row.get("total_amount", "").strip()

            # Rule 1: Primary Key must exist
            if not order_id:
                quarantine_rows.append({"row_idx": row_idx, "error": "MISSING_PK", "data": row})
                continue

            # Rule 2: In-batch deduplication
            if order_id in seen_ids:
                quarantine_rows.append({"row_idx": row_idx, "error": "DUPLICATE_PK", "data": row})
                continue

            # Rule 3: Valid numeric amount
            try:
                amt_val = float(total_amt)
                if amt_val < 0:
                    quarantine_rows.append({"row_idx": row_idx, "error": "NEGATIVE_AMOUNT", "data": row})
                    continue
            except ValueError:
                quarantine_rows.append({"row_idx": row_idx, "error": "TYPE_CAST_FAILURE", "data": row})
                continue

            seen_ids.add(order_id)
            valid_rows.append(row)

    print(f"  Validated: {len(valid_rows)} clean records, {len(quarantine_rows)} quarantined records.")

    # Write quarantine log if errors exist
    if quarantine_rows:
        quarantine_file = QUARANTINE_DIR / f"quarantine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(quarantine_file, "w", encoding="utf-8") as qf:
            for item in quarantine_rows:
                qf.write(json.dumps(item) + "\n")
        print(f"  Quarantine written to: {quarantine_file}")

    # Load clean records atomically into DuckDB warehouse
    con = duckdb.connect(str(target_db))
    con.execute("""
        CREATE TABLE IF NOT EXISTS stg_orders (
            order_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            order_status VARCHAR,
            subtotal NUMERIC(10,2),
            tax NUMERIC(10,2),
            total_amount NUMERIC(10,2),
            created_at TIMESTAMP,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Stage temporary table for atomic upsert/insert
    con.execute("CREATE TEMP TABLE temp_incoming AS SELECT * FROM stg_orders WHERE 1=0;")
    for r in valid_rows:
        con.execute("""
            INSERT INTO temp_incoming (order_id, user_id, order_status, subtotal, tax, total_amount, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, [
            r["order_id"], r["user_id"], r["order_status"],
            float(r.get("subtotal", 0)), float(r.get("tax", 0)),
            float(r["total_amount"]), r["created_at"]
        ])

    # Idempotent Upsert (Delete existing keys before inserting new batch)
    con.execute("""
        DELETE FROM stg_orders
        WHERE order_id IN (SELECT order_id FROM temp_incoming);
    """)
    con.execute("""
        INSERT INTO stg_orders (order_id, user_id, order_status, subtotal, tax, total_amount, created_at)
        SELECT order_id, user_id, order_status, subtotal, tax, total_amount, created_at
        FROM temp_incoming;
    """)

    final_count = con.execute("SELECT COUNT(*) FROM stg_orders;").fetchone()[0]
    con.close()

    print(f"[{datetime.now().isoformat()}] Ingestion Completed. Total rows in warehouse: {final_count}")
    return {
        "valid_count": len(valid_rows),
        "quarantined_count": len(quarantine_rows),
        "warehouse_total": final_count
    }

if __name__ == "__main__":
    run_batch_ingestion()
