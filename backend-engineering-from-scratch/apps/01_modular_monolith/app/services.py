"""
Domain services for Modular Monolith: Users, Catalog, Orders, and Transactional Outbox.
"""

import time
import uuid
import json
import sqlite3
from typing import Dict, Any, List, Optional
from database import Database

class UserService:
    def __init__(self, db: Database):
        self.db = db

    def register_user(self, email: str, password_hash: str) -> Dict[str, Any]:
        user_id = f"usr_{uuid.uuid4().hex[:8]}"
        with self.db.connection() as conn:
            conn.execute(
                "INSERT INTO users (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (user_id, email, password_hash, time.time())
            )
        return {"id": user_id, "email": email}

class CatalogService:
    def __init__(self, db: Database):
        self.db = db

    def add_product(self, name: str, price_cents: int, stock: int) -> Dict[str, Any]:
        prod_id = f"prd_{uuid.uuid4().hex[:8]}"
        with self.db.connection() as conn:
            conn.execute(
                "INSERT INTO products (id, name, price_cents, stock) VALUES (?, ?, ?, ?)",
                (prod_id, name, price_cents, stock)
            )
        return {"id": prod_id, "name": name, "price_cents": price_cents, "stock": stock}

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        with self.db.connection() as conn:
            cur = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if row:
                return dict(row)
        return None

class OrderService:
    def __init__(self, db: Database):
        self.db = db

    def place_order(self, user_id: str, product_id: str, quantity: int) -> Dict[str, Any]:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        order_id = f"ord_{uuid.uuid4().hex[:8]}"
        outbox_id = f"obx_{uuid.uuid4().hex[:8]}"
        now = time.time()

        # Execute atomically within a single transactional boundary
        with self.db.connection() as conn:
            # 1. Pessimistic check of product stock
            cur = conn.execute("SELECT stock, price_cents FROM products WHERE id = ?", (product_id,))
            prod = cur.fetchone()
            if not prod:
                raise KeyError(f"Product {product_id} not found")

            current_stock = prod["stock"]
            if current_stock < quantity:
                raise ValueError(f"Insufficient stock: requested {quantity}, available {current_stock}")

            # 2. Decrement inventory
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (quantity, product_id)
            )

            # 3. Create order
            conn.execute(
                "INSERT INTO orders (id, user_id, product_id, quantity, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, user_id, product_id, quantity, "CONFIRMED", now)
            )

            # 4. Write Transactional Outbox record
            payload = json.dumps({
                "order_id": order_id,
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity,
                "timestamp": now
            })
            conn.execute(
                "INSERT INTO outbox (id, event_type, payload, status, created_at) VALUES (?, ?, ?, ?, ?)",
                (outbox_id, "OrderCreated", payload, "PENDING", now)
            )

        return {
            "order_id": order_id,
            "status": "CONFIRMED",
            "product_id": product_id,
            "quantity": quantity
        }

class OutboxWorker:
    def __init__(self, db: Database):
        self.db = db
        self.dispatched_events: List[Dict[str, Any]] = []

    def process_pending(self, limit: int = 10) -> int:
        processed_count = 0
        with self.db.connection() as conn:
            cur = conn.execute(
                "SELECT id, event_type, payload FROM outbox WHERE status = 'PENDING' LIMIT ?",
                (limit,)
            )
            rows = cur.fetchall()

            for row in rows:
                event_id = row["id"]
                payload = json.loads(row["payload"])
                # Dispatch notification
                self.dispatched_events.append({
                    "event_id": event_id,
                    "event_type": row["event_type"],
                    "payload": payload
                })
                # Update status
                conn.execute(
                    "UPDATE outbox SET status = 'DISPATCHED', processed_at = ? WHERE id = ?",
                    (time.time(), event_id)
                )
                processed_count += 1

        return processed_count
