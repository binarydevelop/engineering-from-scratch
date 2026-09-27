"""
Resilient, production-ready solution for lab-06-unhandled-schema-drift-missing-column.
"""
def parse_payload(payload):
    return {
        "order_id": payload.get("order_id", "UNKNOWN"),
        "tax": float(payload.get("tax", 0.0))
    }
