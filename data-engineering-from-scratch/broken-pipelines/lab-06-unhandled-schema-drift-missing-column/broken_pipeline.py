"""
Broken implementation demonstrating the flaw in lab-06-unhandled-schema-drift-missing-column.
"""
def parse_payload(payload):
    return {"order_id": payload["order_id"], "tax": payload["tax"]} # KeyError if tax missing
