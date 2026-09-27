#!/usr/bin/env python3
import json
import time

def simulate_cdc():
    print("=== Simulating Change Data Capture (Debezium WAL Stream) ===\n")
    # 1. SQL INSERT
    insert_cdc = {
        "op": "c", # Create
        "ts_ms": int(time.time() * 1000),
        "before": None,
        "after": {"order_id": 101, "customer_id": "usr_42", "status": "PENDING"}
    }
    print("1. SQL: INSERT INTO orders VALUES (101, 'usr_42', 'PENDING');")
    print(f"   Kafka CDC Event:\n{json.dumps(insert_cdc, indent=2)}\n")

    # 2. SQL UPDATE
    update_cdc = {
        "op": "u", # Update
        "ts_ms": int(time.time() * 1000),
        "before": {"order_id": 101, "customer_id": "usr_42", "status": "PENDING"},
        "after":  {"order_id": 101, "customer_id": "usr_42", "status": "COMPLETED"}
    }
    print("2. SQL: UPDATE orders SET status = 'COMPLETED' WHERE order_id = 101;")
    print(f"   Kafka CDC Event:\n{json.dumps(update_cdc, indent=2)}\n")

    # 3. SQL DELETE
    delete_cdc = {
        "op": "d", # Delete
        "ts_ms": int(time.time() * 1000),
        "before": {"order_id": 101, "customer_id": "usr_42", "status": "COMPLETED"},
        "after": None
    }
    print("3. SQL: DELETE FROM orders WHERE order_id = 101;")
    print(f"   Kafka CDC Event:\n{json.dumps(delete_cdc, indent=2)}")

if __name__ == "__main__":
    simulate_cdc()
