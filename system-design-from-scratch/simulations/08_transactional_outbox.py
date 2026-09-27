import sqlite3
import json
import time
import uuid
from typing import Dict, Any, List

class TransactionalOutboxManager:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("CREATE TABLE orders (id TEXT PRIMARY KEY, amount INTEGER);")
            self.conn.execute("CREATE TABLE outbox (id TEXT PRIMARY KEY, event_type TEXT, payload TEXT, status TEXT);")

    def create_order(self, amount: int) -> str:
        order_id = f"ord_{uuid.uuid4().hex[:6]}"
        event_id = f"evt_{uuid.uuid4().hex[:6]}"
        payload = json.dumps({"order_id": order_id, "amount": amount})
        # Atomic commit
        with self.conn:
            self.conn.execute("INSERT INTO orders VALUES (?, ?);", (order_id, amount))
            self.conn.execute("INSERT INTO outbox VALUES (?, ?, ?, 'PENDING');", (event_id, "OrderCreated", payload))
        return order_id

    def poll_and_dispatch(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM outbox WHERE status = 'PENDING'")
        rows = cur.fetchall()
        count = len(rows)
        with self.conn:
            for r in rows:
                self.conn.execute("UPDATE outbox SET status = 'DISPATCHED' WHERE id = ?", (r["id"],))
        return count
