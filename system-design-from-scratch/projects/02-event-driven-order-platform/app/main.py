import sqlite3
import json
import time
import uuid
from typing import Dict, Any

class OrderPlatform:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()
        self.dispatched_events = []

    def _init_db(self):
        with self.conn:
            self.conn.execute("CREATE TABLE inventory (item_id TEXT PRIMARY KEY, stock INTEGER);")
            self.conn.execute("CREATE TABLE orders (id TEXT PRIMARY KEY, item_id TEXT, qty INTEGER);")
            self.conn.execute("CREATE TABLE outbox (id TEXT PRIMARY KEY, event_type TEXT, payload TEXT, status TEXT);")
            self.conn.execute("INSERT INTO inventory VALUES ('item_1', 10);")

    def place_order(self, item_id: str, qty: int) -> Dict[str, Any]:
        with self.conn:
            cur = self.conn.execute("SELECT stock FROM inventory WHERE item_id = ?", (item_id,))
            row = cur.fetchone()
            if not row or row["stock"] < qty:
                raise ValueError("Insufficient stock")

            self.conn.execute("UPDATE inventory SET stock = stock - ? WHERE item_id = ?", (qty, item_id))
            order_id = f"ord_{uuid.uuid4().hex[:6]}"
            self.conn.execute("INSERT INTO orders VALUES (?, ?, ?)", (order_id, item_id, qty))

            event_id = f"evt_{uuid.uuid4().hex[:6]}"
            payload = json.dumps({"order_id": order_id, "item_id": item_id, "qty": qty})
            self.conn.execute("INSERT INTO outbox VALUES (?, 'OrderPlaced', ?, 'PENDING')", (event_id, payload))

        return {"order_id": order_id, "status": "CONFIRMED"}

    def outbox_worker(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM outbox WHERE status = 'PENDING'")
        rows = cur.fetchall()
        for r in rows:
            self.dispatched_events.append(dict(r))
            self.conn.execute("UPDATE outbox SET status = 'DISPATCHED' WHERE id = ?", (r["id"],))
        self.conn.commit()
        return len(rows)
