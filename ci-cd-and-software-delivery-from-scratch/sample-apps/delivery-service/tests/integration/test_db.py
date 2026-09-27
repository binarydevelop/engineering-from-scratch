#!/usr/bin/env python3
"""
Integration Tests for Database & Migration Engine
Verifies real database operations, migrations, and transaction safety (Phase 25, 26, 27).
Uses isolated temporary database to guarantee test isolation.
"""

import os
import sqlite3
import tempfile
import unittest
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from db.migration_engine import MigrationEngine


class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_delivery.db")
        self.migrations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../db/migrations"))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_full_migration_lifecycle(self):
        """Verify that running all migrations from scratch sets up tables correctly."""
        engine = MigrationEngine(self.db_path, self.migrations_dir)
        applied = engine.apply_pending()
        self.assertGreaterEqual(applied, 1, "Should have applied at least one migration")

        # Verify idempotency: running again should apply 0
        applied_second_time = engine.apply_pending()
        self.assertEqual(applied_second_time, 0, "Second migration run must be idempotent")

        # Verify table presence and write capability
        conn = sqlite3.connect(self.db_path)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO orders (customer_email, amount_cents, status, created_at, currency) "
                "VALUES ('charlie@example.com', 4500, 'pending', '2026-09-27T00:00:00Z', 'USD')"
            )
            order_id = cur.lastrowid
            cur.execute("SELECT customer_email, amount_cents, currency FROM orders WHERE id = ?", (order_id,))
            row = cur.fetchone()
            self.assertEqual(row[0], "charlie@example.com")
            self.assertEqual(row[1], 4500)
            self.assertEqual(row[2], "USD")
        conn.close()

    def test_test_isolation_guarantee(self):
        """Verify that independent test runs do not see dirty state (Phase 27)."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        # Fresh database has no orders table before migrations
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        self.assertIsNone(cur.fetchone())
        conn.close()


if __name__ == "__main__":
    unittest.main()
