#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
import random

def generate_logs(count=100):
    services = ["auth-api", "payment-api", "cart-api", "shipping-api"]
    levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
    logs = []
    base_time = datetime.utcnow()
    for i in range(count):
        ts = (base_time - timedelta(seconds=i * 5)).isoformat() + "Z"
        svc = random.choice(services)
        lvl = random.choice(levels)
        msg = f"Processed request for order_{i}" if lvl != "ERROR" else "Connection timeout to upstream database"
        logs.append({
            "@timestamp": ts,
            "service": svc,
            "level": lvl,
            "trace_id": f"trace_{random.randint(1000, 9999)}",
            "message": msg,
            "duration_ms": random.randint(10, 450)
        })
    return logs

if __name__ == "__main__":
    data = generate_logs(5)
    print("Capstone 2: Structured Log Event Format:")
    print(json.dumps(data, indent=2))
