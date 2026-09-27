#!/usr/bin/env python3
"""
projects/log_search/generator.py - Ingests synthetic microservice logs into Elasticsearch.
"""

import json
import os
import random
import sys
import time
import urllib.request
from datetime import datetime, timedelta

ES_HOST = os.environ.get("ES_URL", "http://localhost:9200")
INDEX_NAME = "microservice_logs"
DIR = os.path.dirname(os.path.abspath(__file__))

def init_index():
    with open(os.path.join(DIR, "schema.json"), "r") as f:
        schema = json.load(f)
    req = urllib.request.Request(f"{ES_HOST}/{INDEX_NAME}", method="DELETE")
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass
    req = urllib.request.Request(f"{ES_HOST}/{INDEX_NAME}", data=json.dumps(schema).encode(), headers={"Content-Type": "application/json"}, method="PUT")
    urllib.request.urlopen(req)
    print(f"Created index '{INDEX_NAME}'.")

def generate_and_ship_logs(count=1000):
    services = ["auth-api", "payment-api", "inventory-api", "order-api", "notification-api"]
    levels = ["INFO", "INFO", "INFO", "INFO", "WARN", "ERROR"]
    error_messages = [
        "Database pool exhausted",
        "Upstream payment gateway timed out",
        "Redis connection reset by peer",
        "Kafka partition leader not available"
    ]
    base_time = datetime.utcnow()
    lines = []

    for i in range(count):
        lvl = random.choice(levels)
        svc = random.choice(services)
        ts = (base_time - timedelta(minutes=random.randint(0, 120), seconds=random.randint(0, 59))).isoformat() + "Z"
        status = 200 if lvl == "INFO" else (400 if lvl == "WARN" else 500)
        msg = f"Processed request for entity {random.randint(1000, 9999)}" if lvl != "ERROR" else random.choice(error_messages)

        doc = {
            "@timestamp": ts,
            "service": svc,
            "level": lvl,
            "trace_id": f"trace_{random.randint(100000, 999999)}",
            "status_code": status,
            "duration_ms": random.randint(5, 800),
            "message": msg
        }
        lines.append(json.dumps({"index": {"_index": INDEX_NAME}}))
        lines.append(json.dumps(doc))

    payload = "\n".join(lines) + "\n"
    req = urllib.request.Request(f"{ES_HOST}/_bulk?refresh=true", data=payload.encode("utf-8"), headers={"Content-Type": "application/x-ndjson"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Successfully shipped {count} logs to Elasticsearch. Errors: {res.get('errors')}")

if __name__ == "__main__":
    init_index()
    generate_and_ship_logs(500)
