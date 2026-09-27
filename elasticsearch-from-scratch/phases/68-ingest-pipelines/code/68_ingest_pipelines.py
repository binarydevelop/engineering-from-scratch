#!/usr/bin/env python3
import re

def simulate_ingest_pipeline(raw_doc):
    message = raw_doc.get("message", "")
    pattern = r"(?P<ip>\S+) (?P<method>\S+) (?P<path>\S+) (?P<status>\d+)"
    match = re.match(pattern, message)
    if not match:
        return {"error": "grok_parse_failure", "raw": message}

    data = match.groupdict()
    data["status"] = int(data["status"])
    return data

if __name__ == "__main__":
    sample = {"message": "192.168.1.42 POST /api/v2/orders 201"}
    print("Raw Incoming Document:")
    print(" ", sample)
    transformed = simulate_ingest_pipeline(sample)
    print("\nTransformed Document after Ingest Pipeline:")
    print(" ", transformed)
