#!/usr/bin/env python3
"""
pipelines/incremental_cdc.py
Incremental CDC (Change Data Capture) Pipeline:
Simulates consumption of a database Write-Ahead Log (WAL) stream.
Applies INSERT, UPDATE, DELETE mutations to target analytical store and maintains durable checkpoints.
"""
import os
import json
import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "datasets" / "raw"
DATA_DIR = BASE_DIR / "data" / "warehouse"
CHECKPOINT_FILE = DATA_DIR / "cdc_checkpoint.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f).get("last_lsn", 0)
    return 0

def save_checkpoint(last_lsn):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_lsn": last_lsn}, f)

def run_cdc_pipeline(stream_file=None, target_db=None):
    if stream_file is None:
        stream_file = RAW_DIR / "cdc_wal_stream.jsonl"
    if target_db is None:
        target_db = DATA_DIR / "analytics.duckdb"

    last_lsn = load_checkpoint()
    print(f"Starting CDC consumer from checkpoint LSN: {last_lsn}")

    con = duckdb.connect(str(target_db))
    con.execute("""
        CREATE TABLE IF NOT EXISTS orders_replica (
            order_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            status VARCHAR,
            amount NUMERIC(10,2),
            last_replicated_lsn BIGINT
        );
    """)

    mutations_applied = 0
    current_lsn = last_lsn

    with open(stream_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            event_lsn = event["lsn"]

            # Skip events already committed before checkpoint
            if event_lsn <= last_lsn:
                continue

            op = event["op"]
            table = event["table"]

            if table == "orders":
                if op == "INSERT":
                    after = event["after"]
                    con.execute("""
                        INSERT INTO orders_replica (order_id, user_id, status, amount, last_replicated_lsn)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT (order_id) DO UPDATE SET
                            status = excluded.status,
                            amount = excluded.amount,
                            last_replicated_lsn = excluded.last_replicated_lsn;
                    """, [after["order_id"], after["user_id"], after["status"], after["amount"], event_lsn])
                    mutations_applied += 1

                elif op == "UPDATE":
                    after = event["after"]
                    con.execute("""
                        UPDATE orders_replica
                        SET status = ?, amount = ?, last_replicated_lsn = ?
                        WHERE order_id = ?;
                    """, [after["status"], after["amount"], event_lsn, after["order_id"]])
                    mutations_applied += 1

                elif op == "DELETE":
                    before = event["before"]
                    con.execute("""
                        DELETE FROM orders_replica
                        WHERE order_id = ?;
                    """, [before["order_id"]])
                    mutations_applied += 1

            current_lsn = max(current_lsn, event_lsn)

    save_checkpoint(current_lsn)
    replica_count = con.execute("SELECT COUNT(*) FROM orders_replica;").fetchone()[0]
    con.close()

    print(f"CDC pipeline applied {mutations_applied} mutations. Replica rows: {replica_count}. New LSN: {current_lsn}")
    return {
        "mutations_applied": mutations_applied,
        "replica_count": replica_count,
        "committed_lsn": current_lsn
    }

if __name__ == "__main__":
    run_cdc_pipeline()
