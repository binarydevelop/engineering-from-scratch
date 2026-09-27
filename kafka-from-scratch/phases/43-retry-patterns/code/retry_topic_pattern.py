#!/usr/bin/env python3
import time

def simulate_retry_pipeline():
    print("--- Simulating Non-Blocking Retry Topic Pipeline ---")
    events = [
        {"id": "ORD-1", "status": "valid"},
        {"id": "ORD-2", "status": "transient_fail"},
        {"id": "ORD-3", "status": "valid"},
    ]

    main_topic = "orders"
    retry_topic_1 = "orders.RETRY-1"

    for ev in events:
        print(f"\n[Main Consumer] Processing {ev['id']} from '{main_topic}'...")
        if ev["status"] == "valid":
            print(f"  [SUCCESS] Order {ev['id']} processed! Committing offset.")
        else:
            print(f"  [TRANSIENT FAILURE] Downstream API 503 for {ev['id']}!")
            print(f"  -> Forwarding {ev['id']} to '{retry_topic_1}' with header retry_count=1")
            print(f"  -> Committing offset on '{main_topic}'! Main consumer DOES NOT BLOCK!")

    print("\n[Retry Consumer] Wakes up after 5s backoff delay...")
    print(f"  -> Fetches ORD-2 from '{retry_topic_1}'")
    print("  -> Downstream API recovered: [SUCCESS] ORD-2 processed!")

if __name__ == "__main__":
    simulate_retry_pipeline()
