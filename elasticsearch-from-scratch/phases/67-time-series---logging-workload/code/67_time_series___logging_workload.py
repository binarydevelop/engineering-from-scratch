#!/usr/bin/env python3
from datetime import datetime, timedelta

def generate_sample_log(service, level, msg, hours_ago=0):
    ts = (datetime.utcnow() - timedelta(hours=hours_ago)).isoformat() + "Z"
    return {
        "@timestamp": ts,
        "service": service,
        "level": level,
        "message": msg
    }

if __name__ == "__main__":
    logs = [
        generate_sample_log("auth-svc", "INFO", "User login successful", hours_ago=1),
        generate_sample_log("payment-svc", "ERROR", "Payment gateway timeout", hours_ago=2),
        generate_sample_log("auth-svc", "WARN", "Invalid password attempt", hours_ago=3)
    ]
    print("Generated Structured Time-Series Log Records:")
    for l in logs:
        print(f"  [{l['@timestamp']}] [{l['level']:5s}] {l['service']:12s}: {l['message']}")
