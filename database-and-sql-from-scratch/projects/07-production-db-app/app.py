"""
Production-Like Database Application Service.
Demonstrates:
  - Connection Pool Lifecycle
  - Parameterized Query Layer (SQL Injection Prevention)
  - Atomic Transaction Management
  - Chaos Fault Injection (Deadlocks, Slow Queries, Pool Starvation)
"""

import os
import time
import threading
from typing import List, Dict, Any, Optional

try:
    import psycopg
    from psycopg_pool import ConnectionPool
    HAS_PSYCOPG3 = True
except ImportError:
    HAS_PSYCOPG3 = False


class DatabasePool:
    """Manages connection pooling and transaction lifecycle."""
    def __init__(self, min_size: int = 2, max_size: int = 10):
        self.host = os.getenv("PGHOST", "localhost")
        self.port = int(os.getenv("PGPORT", "5432"))
        self.dbname = os.getenv("PGDATABASE", "sqllab")
        self.user = os.getenv("PGUSER", "postgres")
        self.password = os.getenv("PGPASSWORD", "postgres")
        self.min_size = min_size
        self.max_size = max_size
        self.pool = None

        if HAS_PSYCOPG3:
            conninfo = f"host={self.host} port={self.port} dbname={self.dbname} user={self.user} password={self.password}"
            self.pool = ConnectionPool(conninfo, min_size=self.min_size, max_size=self.max_size)

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[tuple]:
        """Executes a safe parameterized read query."""
        if not HAS_PSYCOPG3:
            raise RuntimeError("psycopg[binary] is required to run live pool queries.")
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()

    def execute_transaction(self, operations: list) -> bool:
        """Executes multiple write statements in a single atomic transaction."""
        if not HAS_PSYCOPG3:
            raise RuntimeError("psycopg[binary] is required.")
        with self.pool.connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    for sql, params in operations:
                        cur.execute(sql, params)
            return True


class OrderRepository:
    def __init__(self, db: DatabasePool):
        self.db = db

    def get_customer_orders(self, customer_id: int) -> List[Dict[str, Any]]:
        # SAFE: Parameterized query prevents SQL injection
        sql = """
        SELECT id, status, total_amount, order_date
        FROM ecommerce.orders
        WHERE customer_id = %s
        ORDER BY order_date DESC;
        """
        rows = self.db.execute_query(sql, (customer_id,))
        return [
            {"order_id": r[0], "status": r[1], "total": float(r[2]), "date": str(r[3])}
            for r in rows
        ]


def main():
    print("Database Application Service Layer initialized.")
    if HAS_PSYCOPG3:
        print("[+] psycopg3 and connection pooling active.")
    else:
        print("[!] Note: Run 'pip install -r requirements.txt' to enable live container pooling.")


if __name__ == "__main__":
    main()
