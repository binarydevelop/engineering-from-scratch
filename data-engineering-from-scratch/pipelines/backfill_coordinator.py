#!/usr/bin/env python3
"""
pipelines/backfill_coordinator.py
Historical Backfill Engine:
Safely reprocesses historical partitioned data slices across an arbitrary date range.
Employs atomic partition replacement to avoid downtime or corrupted intermediate reads.
"""
import sys
import datetime
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "warehouse"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class BackfillCoordinator:
    def __init__(self, db_path=None):
        self.db_path = db_path or (DATA_DIR / "backfill_analytics.duckdb")
        self.con = duckdb.connect(str(self.db_path))
        self._init_tables()

    def _init_tables(self):
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS daily_sales_partitioned (
                order_date DATE,
                order_id VARCHAR,
                amount NUMERIC(10,2),
                version_id INTEGER,
                PRIMARY KEY (order_date, order_id)
            );
        """)

    def execute_partition_backfill(self, target_date, version_id=2):
        date_str = target_date.isoformat()
        print(f"  [Backfill] Processing partition: {date_str} (Version: {version_id})...")

        # Simulate generating updated historical data for that day
        updated_records = [
            (date_str, f"ord_{date_str}_01", 120.0, version_id),
            (date_str, f"ord_{date_str}_02", 340.5, version_id),
            (date_str, f"ord_{date_str}_03", 85.0, version_id),
        ]

        # Atomic Partition Replacement:
        # Delete only the specific partition slice, then insert newly computed records
        self.con.execute("BEGIN TRANSACTION;")
        self.con.execute("DELETE FROM daily_sales_partitioned WHERE order_date = ?;", [date_str])
        self.con.executemany("""
            INSERT INTO daily_sales_partitioned (order_date, order_id, amount, version_id)
            VALUES (?, ?, ?, ?);
        """, updated_records)
        self.con.execute("COMMIT;")

    def run_range_backfill(self, start_date_str, end_date_str, version_id=2):
        start_dt = datetime.date.fromisoformat(start_date_str)
        end_dt = datetime.date.fromisoformat(end_date_str)

        print(f"Starting Historical Backfill from {start_dt} to {end_dt}...")
        current_dt = start_dt
        partitions_processed = 0

        while current_dt <= end_dt:
            self.execute_partition_backfill(current_dt, version_id=version_id)
            current_dt += datetime.timedelta(days=1)
            partitions_processed += 1

        total_rows = self.con.execute("SELECT COUNT(*) FROM daily_sales_partitioned;").fetchone()[0]
        print(f"Backfill finished. {partitions_processed} partitions updated. Total records: {total_rows}")
        return partitions_processed, total_rows

    def close(self):
        self.con.close()

if __name__ == "__main__":
    coordinator = BackfillCoordinator()
    coordinator.run_range_backfill("2026-09-01", "2026-09-05", version_id=1)
    # Re-run backfill with updated version_id to prove safe historical replay
    coordinator.run_range_backfill("2026-09-02", "2026-09-03", version_id=2)
    coordinator.close()
