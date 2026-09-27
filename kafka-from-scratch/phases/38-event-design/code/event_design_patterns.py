#!/usr/bin/env python3
import uuid
import time
import json

def create_domain_event(entity_id: str, event_type: str, payload: dict) -> dict:
    """Standard Production Event Envelope."""
    return {
        "metadata": {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "schema_version": "1.0",
            "timestamp": int(time.time() * 1000),
            "source_service": "checkout-service",
            "correlation_id": str(uuid.uuid4())
        },
        "key": entity_id,
        "data": payload
    }

if __name__ == "__main__":
    event = create_domain_event(
        entity_id="order-9901",
        event_type="OrderPlaced",
        payload={
            "order_id": "order-9901",
            "customer_id": "usr_42",
            "currency": "USD",
            "amount": 149.99,
            "items": [{"sku": "HEADPHONES-PRO", "qty": 1, "price": 149.99}]
        }
    )
    print("Standard Production Event Envelope:")
    print(json.dumps(event, indent=2))
