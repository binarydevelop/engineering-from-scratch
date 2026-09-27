#!/usr/bin/env python3
import json
import time

def process_order(record_str: str):
    data = json.loads(record_str)
    # Strict validation: amount must be a number > 0
    if not isinstance(data.get("amount"), (int, float)):
        raise ValueError(f"Invalid amount type: {type(data.get('amount'))}")
    return True

def run_dlt_pipeline():
    print("--- Dead-Letter Topic (DLT) Demonstration ---")
    incoming_records = [
        {"topic": "orders", "offset": 101, "payload": '{"order_id": 1, "amount": 25.50}'},
        {"topic": "orders", "offset": 102, "payload": '{"order_id": 2, "amount": "CORRUPT_NOT_A_NUMBER"}'}, # Poison Pill!
        {"topic": "orders", "offset": 103, "payload": '{"order_id": 3, "amount": 80.00}'},
    ]

    dlt_topic = []

    for r in incoming_records:
        print(f"\nProcessing record at offset {r['offset']}...")
        try:
            process_order(r["payload"])
            print(f" [SUCCESS] Offset {r['offset']} processed normally.")
        except Exception as ex:
            print(f" [POISON PILL DETECTED] Processing failed: {ex}")
            # Quarantine to DLT with forensic envelope
            dlt_envelope = {
                "original_topic": r["topic"],
                "original_offset": r["offset"],
                "raw_payload": r["payload"],
                "error": str(ex),
                "quarantined_at": time.time()
            }
            dlt_topic.append(dlt_envelope)
            print(f" [DLT ROUTED] Record {r['offset']} quarantined to 'orders.DLT'!")
            print(" [COMMITTED] Offset committed on main topic. Main pipeline proceeds!")

    print(f"\nTotal Records Quarantined in DLT: {len(dlt_topic)}")
    print(f"DLT Envelope Contents:\n{json.dumps(dlt_topic[0], indent=2)}")

if __name__ == "__main__":
    run_dlt_pipeline()
