#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = "/tmp/idempotent_lab.db"

class IdempotentOrderConsumer:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        if os.path.exists(self.db_path): os.remove(self.db_path)
        conn = sqlite3.connect(self.db_path)
        # Business table
        conn.execute("CREATE TABLE orders (order_id TEXT PRIMARY KEY, amount REAL)")
        # Idempotency table
        conn.execute("CREATE TABLE processed_events (event_id TEXT PRIMARY KEY, processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()

    def process_record(self, event_id: str, order_id: str, amount: float):
        conn = sqlite3.connect(self.db_path)
        try:
            # ATOMIC TRANSACTION: Check idempotency + execute business write together
            with conn:
                cursor = conn.cursor()
                # Check if event was already handled
                cursor.execute("SELECT 1 FROM processed_events WHERE event_id = ?", (event_id,))
                if cursor.fetchone() is not None:
                    print(f" [DUPLICATE DETECTED] Event {event_id} already processed. SKIPPING side effect!")
                    return False

                # Execute business write
                cursor.execute("INSERT INTO orders (order_id, amount) VALUES (?, ?)", (order_id, amount))
                # Record idempotency key
                cursor.execute("INSERT INTO processed_events (event_id) VALUES (?)", (event_id,))
                print(f" [PROCESSED] Successfully executed order {order_id} for ${amount:.2f}")
                return True
        finally:
            conn.close()

if __name__ == "__main__":
    consumer = IdempotentOrderConsumer()
    
    # Simulate receiving the exact same event 3 times (due to retries / crashes)
    event = {"event_id": "evt_uuid_12345", "order_id": "ORD-501", "amount": 99.95}

    print("Delivery 1:")
    consumer.process_record(event["event_id"], event["order_id"], event["amount"])

    print("\nDelivery 2 (Duplicate replay):")
    consumer.process_record(event["event_id"], event["order_id"], event["amount"])

    print("\nDelivery 3 (Duplicate replay):")
    consumer.process_record(event["event_id"], event["order_id"], event["amount"])

    conn = sqlite3.connect(DB_PATH)
    orders = conn.execute("SELECT * FROM orders").fetchall()
    print(f"\nFinal Database Orders: {orders}")
    print("Result: Exactly 1 order in database despite 3 deliveries!")
    conn.close()
