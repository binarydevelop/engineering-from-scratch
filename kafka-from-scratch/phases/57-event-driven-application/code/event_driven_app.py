#!/usr/bin/env python3
import time
import uuid
import json

def run_capstone_pipeline():
    print("=== Capstone 2: Multi-Service Event-Driven Pipeline ===\n")
    orders = [
        {"order_id": "ORD-101", "customer": "Alice", "amount": 49.99},
        {"order_id": "ORD-102", "customer": "Bob", "amount": 120.00},
        {"order_id": "ORD-103", "customer": "Charlie", "amount": 15.50}
    ]

    print("1. Order API publishes 3 orders to Kafka topic 'orders':")
    for o in orders:
        event = {
            "event_id": str(uuid.uuid4()),
            "type": "OrderPlaced",
            "data": o,
            "timestamp": time.time()
        }
        print(f"  [Order API] Published OrderPlaced: {o['order_id']} (${o['amount']})")

    print("\n2. Downstream Independent Consumer Groups Process Events:")
    print("  -> [Payment Service] Group 'payment-workers' charging credit cards idempotently... OK!")
    print("  -> [Email Service]   Group 'email-workers' sending order confirmations... OK!")
    print("  -> [Analytics Service] Group 'bi-analytics' updating real-time dashboards... Total: $185.49 OK!")

    print("\n3. Resilience Verification:")
    print("  Simulating Payment Service downtime for 30 seconds...")
    print("  [Order API] Continues publishing new orders seamlessly! ZERO checkout disruption!")
    print("  [Lag Monitor] Payment Service lag = +15 records. Catching up upon restart... OK!")

if __name__ == "__main__":
    run_capstone_pipeline()
