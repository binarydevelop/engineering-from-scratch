#!/usr/bin/env python3
import sqlite3
import os
import uuid
import json

DB_PATH = "/tmp/outbox_lab.db"

def init_db():
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE orders (order_id TEXT PRIMARY KEY, amount REAL)")
    conn.execute("""
        CREATE TABLE outbox_events (
            event_id TEXT PRIMARY KEY,
            event_type TEXT,
            payload TEXT,
            published INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def place_order_with_outbox(order_id: str, amount: float):
    conn = sqlite3.connect(DB_PATH)
    try:
        # ATOMIC LOCAL TRANSACTION: Business write + Outbox write together!
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO orders VALUES (?, ?)", (order_id, amount))
            event_payload = json.dumps({"order_id": order_id, "amount": amount})
            cursor.execute("INSERT INTO outbox_events VALUES (?, ?, ?, 0)",
                           (str(uuid.uuid4()), "OrderPlaced", event_payload))
        print(f" [DB TX COMMITTED] Order {order_id} + Outbox Event committed atomically!")
        return True
    except Exception as e:
        print(f" [DB TX ROLLED BACK] Failed: {e}")
        return False
    finally:
        conn.close()

def relay_outbox_to_kafka():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT event_id, event_type, payload FROM outbox_events WHERE published = 0")
    pending = cursor.fetchall()
    print(f"\n[Relay Poller] Found {len(pending)} unpublished events in outbox:")
    for eid, etype, payload in pending:
        # Simulate publishing to Kafka
        print(f"  -> Publishing {etype} ({eid}) to Kafka... Ack received!")
        # Mark as published
        cursor.execute("UPDATE outbox_events SET published = 1 WHERE event_id = ?", (eid,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    place_order_with_outbox("ORD-901", 89.50)
    place_order_with_outbox("ORD-902", 145.00)
    relay_outbox_to_kafka()
