#!/usr/bin/env python3
import json

def legacy_consumer_v1(raw_payload: str):
    data = json.loads(raw_payload)
    # Expects strict schema v1: user_id (int), email (str)
    try:
        user_id = data["user_id"]
        email = data["email"]
        print(f" [Consumer v1 OK] Handled user_id={user_id}, email={email}")
    except KeyError as e:
        print(f" [Consumer v1 CRASHED!] Missing required key: {e}")

def resilient_consumer_v2(raw_payload: str):
    data = json.loads(raw_payload)
    # Resilient schema: handles both user_id and customer_uuid, default loyalty_tier
    uid = data.get("customer_uuid") or data.get("user_id", "UNKNOWN")
    email = data.get("email", "no-email@provided")
    tier = data.get("loyalty_tier", "STANDARD")
    print(f" [Consumer v2 OK] Handled uid={uid}, email={email}, tier={tier}")

if __name__ == "__main__":
    print("--- 1. Producer sends v1 payload ---")
    p1 = json.dumps({"user_id": 101, "email": "alice@example.com"})
    legacy_consumer_v1(p1)

    print("\n--- 2. Producer evolves schema to v2 (Renames user_id to customer_uuid) ---")
    p2_broken = json.dumps({"customer_uuid": "CUST-99", "email": "bob@example.com", "loyalty_tier": "VIP"})
    legacy_consumer_v1(p2_broken) # CRASHES!

    print("\n--- 3. Resilient Consumer handles both v1 and v2 seamlessly ---")
    resilient_consumer_v2(p1)
    resilient_consumer_v2(p2_broken)
