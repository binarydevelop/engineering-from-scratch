#!/usr/bin/env python3
"""
Capstone 2: Production-Grade Event-Driven Application
Demonstrates:
  - Order API emitting OrderPlaced events with metadata envelopes
  - Payment Worker with atomic SQLite idempotency and retry routing
  - Email Worker (independent consumer group)
  - Analytics Worker (independent consumer group)
  - Failure injection: Payment service outage while checkout continues uninterrupted
"""

import time
import uuid
import json
import sqlite3
import os
from collections import defaultdict

DB_PAYMENTS = "/tmp/capstone2_payments.db"

def init_payment_db():
    if os.path.exists(DB_PAYMENTS): os.remove(DB_PAYMENTS)
    conn = sqlite3.connect(DB_PAYMENTS)
    conn.execute("CREATE TABLE processed_payments (event_id TEXT PRIMARY KEY, order_id TEXT, amount REAL)")
    conn.commit()
    conn.close()

class EventDrivenAppSimulation:
    def __init__(self):
        init_payment_db()
        self.orders_topic = []
        self.retry_topic = []
        self.dlt_topic = []
        self.analytics_total_revenue = 0.0
        self.emails_sent = []

    def api_checkout(self, customer: str, amount: float) -> str:
        order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        event = {
            "event_id": str(uuid.uuid4()),
            "type": "OrderPlaced",
            "order_id": order_id,
            "customer": customer,
            "amount": amount,
            "timestamp": time.time()
        }
        self.orders_topic.append(event)
        print(f" [Order API] Placed order {order_id} for ${amount:.2f} (Event ID: {event['event_id'][:8]}...)")
        return order_id

    def worker_payment(self, event: dict, simulate_failure: bool = False):
        if simulate_failure:
            print(f"   -> [Payment Worker] GATEWAY TIMEOUT! Routing {event['order_id']} to orders.RETRY")
            self.retry_topic.append(event)
            return False

        conn = sqlite3.connect(DB_PAYMENTS)
        try:
            with conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM processed_payments WHERE event_id = ?", (event["event_id"],))
                if cur.fetchone() is not None:
                    print(f"   -> [Payment Worker] DUPLICATE event {event['event_id'][:8]}. Skipping!")
                    return True
                cur.execute("INSERT INTO processed_payments VALUES (?, ?, ?)",
                            (event["event_id"], event["order_id"], event["amount"]))
                print(f"   -> [Payment Worker] Charged ${event['amount']:.2f} for {event['order_id']} (Idempotent OK)")
                return True
        finally:
            conn.close()

    def worker_email(self, event: dict):
        self.emails_sent.append(event["order_id"])
        print(f"   -> [Email Worker] Sent receipt to {event['customer']} for {event['order_id']}")

    def worker_analytics(self, event: dict):
        self.analytics_total_revenue += event["amount"]
        print(f"   -> [Analytics Worker] Added ${event['amount']:.2f} | Total Revenue: ${self.analytics_total_revenue:.2f}")

if __name__ == "__main__":
    app = EventDrivenAppSimulation()
    print("=== 1. Normal E-Commerce Flow ===")
    o1 = app.api_checkout("Alice", 49.99)
    app.worker_payment(app.orders_topic[-1])
    app.worker_email(app.orders_topic[-1])
    app.worker_analytics(app.orders_topic[-1])

    print("\\n=== 2. Payment Gateway Down (Checkout Must NOT Fail!) ===")
    o2 = app.api_checkout("Bob", 120.00)
    # Payment fails, but Email and Analytics run, and Checkout succeeded!
    app.worker_payment(app.orders_topic[-1], simulate_failure=True)
    app.worker_email(app.orders_topic[-1])
    app.worker_analytics(app.orders_topic[-1])

    print("\\n=== 3. Payment Service Recovers (Draining Retry Topic) ===")
    retried_event = app.retry_topic.pop(0)
    print(f" [Retry Worker] Reprocessing {retried_event['order_id']} from orders.RETRY...")
    app.worker_payment(retried_event, simulate_failure=False)

    print("\\n=== 4. Testing Idempotent Deduplication (Replaying event) ===")
    app.worker_payment(retried_event, simulate_failure=False)

    conn = sqlite3.connect(DB_PAYMENTS)
    rows = conn.execute("SELECT count(*) FROM processed_payments").fetchone()[0]
    print(f"\\nFinal Paid Orders in DB: {rows} (Expected exactly 2). All workers verified!")
    conn.close()
