#!/usr/bin/env python3
import json

def generate_reassignment_plan():
    print("=== Generating Partition Reassignment Plan ===")
    plan = {
        "version": 1,
        "partitions": [
            {"topic": "replicated-orders", "partition": 0, "replicas": [2, 3], "log_dirs": ["any", "any"]},
            {"topic": "replicated-orders", "partition": 1, "replicas": [3, 1], "log_dirs": ["any", "any"]},
            {"topic": "replicated-orders", "partition": 2, "replicas": [1, 2], "log_dirs": ["any", "any"]}
        ]
    }
    plan_json = json.dumps(plan, indent=2)
    print(f"Reassignment JSON Payload:\n{plan_json}")
    with open("/tmp/reassign_plan.json", "w") as f:
        f.write(plan_json)
    print("\nSaved to /tmp/reassign_plan.json. Ready for execution via kafka-reassign-partitions.sh")

if __name__ == "__main__":
    generate_reassignment_plan()
