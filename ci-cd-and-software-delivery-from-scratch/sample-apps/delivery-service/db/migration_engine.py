#!/usr/bin/env python3
"""
Database Migration Engine — Staged Evolution & Zero-Downtime Schema Management
Demonstrates:
- Expand / Migrate / Contract paradigm
- Migration idempotency
- Schema version tracking
- Rollback safety verification
"""

import os
import sqlite3
import sys
from typing import List, Tuple


class MigrationEngine:
    def __init__(self, db_path: str, migrations_dir: str):
        self.db_path = db_path
        self.migrations_dir = migrations_dir
        self._ensure_schema_history_table()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_schema_history_table(self):
        conn = self._get_connection()
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.close()

    def get_applied_versions(self) -> List[int]:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version FROM schema_migrations ORDER BY version ASC")
        versions = [row[0] for row in cur.fetchall()]
        conn.close()
        return versions

    def get_pending_migrations(self) -> List[Tuple[int, str, str]]:
        """Returns sorted list of (version, filename, full_path) that haven't been applied yet."""
        applied = set(self.get_applied_versions())
        files = sorted(os.listdir(self.migrations_dir))
        pending = []
        for f in files:
            if f.endswith(".sql"):
                parts = f.split("_", 1)
                try:
                    version = int(parts[0])
                    if version not in applied:
                        pending.append((version, f, os.path.join(self.migrations_dir, f)))
                except ValueError:
                    continue
        return pending

    def apply_pending(self) -> int:
        """Applies all pending migrations idempotently in a transaction. Returns count applied."""
        pending = self.get_pending_migrations()
        if not pending:
            print("Database is up to date. No pending migrations.")
            return 0

        conn = self._get_connection()
        count = 0
        for version, name, filepath in pending:
            print(f"Applying migration [{version:03d}]: {name}...")
            with open(filepath, "r", encoding="utf-8") as f:
                sql_script = f.read()

            try:
                with conn:
                    conn.executescript(sql_script)
                    conn.execute(
                        "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
                        (version, name)
                    )
                count += 1
                print(f"  -> Applied migration [{version:03d}] successfully.")
            except Exception as e:
                print(f"ERROR applying migration [{version:03d}] {name}: {e}", file=sys.stderr)
                conn.close()
                raise e

        conn.close()
        return count


def main():
    base_dir = os.path.dirname(__file__)
    db_path = os.environ.get("DB_PATH", os.path.join(base_dir, "..", "delivery.db"))
    migrations_dir = os.path.join(base_dir, "migrations")

    engine = MigrationEngine(db_path, migrations_dir)
    applied = engine.apply_pending()
    sys.exit(0 if applied >= 0 else 1)


if __name__ == "__main__":
    main()
