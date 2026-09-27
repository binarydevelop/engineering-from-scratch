#!/usr/bin/env python3
"""
state_recorder.py
Writes and reads timestamped records from /data/state.json.
Used to demonstrate data persistence across container destruction.
"""

import json
import os
import sys
import time

STATE_FILE = "/data/state.json"

def write_record(record_text: str):
    os.makedirs("/data", exist_ok=True)
    records = []
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                records = json.load(f)
        except Exception:
            records = []

    new_entry = {
        "timestamp": time.time(),
        "record": record_text,
        "pid": os.getpid(),
    }
    records.append(new_entry)
    
    with open(STATE_FILE, "w") as f:
        json.dump(records, f, indent=2)
    print(f"Recorded: '{record_text}' into {STATE_FILE} (Total records: {len(records)})")

def read_records():
    if not os.path.exists(STATE_FILE):
        print(f"[EMPTY] {STATE_FILE} does not exist. No persistent state found!")
        sys.exit(1)
        
    with open(STATE_FILE, "r") as f:
        records = json.load(f)
        
    print(f"=== Found {len(records)} Persistent Record(s) in {STATE_FILE} ===")
    for idx, r in enumerate(records):
        print(f"  [{idx+1}] {r['record']} (recorded at {r['timestamp']})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: state_recorder.py [write <TEXT> | read]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "write":
        text = sys.argv[2] if len(sys.argv) > 2 else "Default Record"
        write_record(text)
    elif cmd == "read":
        read_records()
