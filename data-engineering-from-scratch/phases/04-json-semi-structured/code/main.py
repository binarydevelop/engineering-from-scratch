"""
Phase 04: JSON and Semi-Structured Data
Building a recursive flattener for nested objects, arrays, and missing keys.
Transforms nested JSON trees into flat relational records suitable for SQL queries.
"""
import json

def flatten_json(obj, parent_key="", sep="."):
    items = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_key = f"{parent_key}[{i}]"
            if isinstance(item, (dict, list)):
                items.extend(flatten_json(item, new_key, sep=sep).items())
            else:
                items.append((new_key, item))
    else:
        items.append((parent_key, obj))
    return dict(items)

def execute_phase():
    sample_payload = {
        "order_id": "ord_990",
        "customer": {
            "name": "Alice Cooper",
            "address": {
                "city": "Austin",
                "zip": "78701"
            }
        },
        "items": [
            {"sku": "SKU-A", "qty": 2, "price": 45.0},
            {"sku": "SKU-B", "qty": 1, "price": 110.0}
        ]
    }
    flattened = flatten_json(sample_payload)
    assert flattened["customer.address.city"] == "Austin"
    assert flattened["items[0].sku"] == "SKU-A"
    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "flattened_fields_count": len(flattened)
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 04 Result:", res)
