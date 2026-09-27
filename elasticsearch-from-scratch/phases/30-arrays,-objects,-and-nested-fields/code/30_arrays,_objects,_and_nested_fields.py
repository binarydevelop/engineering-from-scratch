#!/usr/bin/env python3

def standard_flatten_match(doc, query_first, query_last):
    # Standard Lucene flattening: parallel lists
    flat_first = [u["first"] for u in doc["users"]]
    flat_last = [u["last"] for u in doc["users"]]
    return (query_first in flat_first) and (query_last in flat_last)

def nested_match(doc, query_first, query_last):
    # Enforces intra-object correlation
    for u in doc["users"]:
        if u["first"] == query_first and u["last"] == query_last:
            return True
    return False

if __name__ == "__main__":
    doc = {
        "id": 1,
        "users": [
            {"first": "Alice", "last": "Smith"},
            {"first": "Bob", "last": "Jones"}
        ]
    }
    q_f, q_l = "Alice", "Jones"
    print(f"Document Users: {doc['users']}")
    print(f"Querying: first='{q_f}' AND last='{q_l}':")
    print(f"  Standard Flattened Match? {standard_flatten_match(doc, q_f, q_l)} (FALSE POSITIVE!)")
    print(f"  Nested Correlated Match?  {nested_match(doc, q_f, q_l)} (CORRECTLY REJECTED)")
