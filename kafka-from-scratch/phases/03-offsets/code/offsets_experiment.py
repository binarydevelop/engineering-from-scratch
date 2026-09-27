#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
import sys

# Import MiniLog from Phase 02
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

OFFSET_STORE = "/tmp/consumer_offset.json"

def load_consumer_offset():
    if os.path.exists(OFFSET_STORE):
        with open(OFFSET_STORE, "r") as f:
            return json.load(f).get("offset", 0)
    return 0

def save_consumer_offset(offset):
    with open(OFFSET_STORE, "w") as f:
        json.dump({"offset": offset}, f)

def simulate_consumer(log, mode="commit_after", crash_at=None):
    current_pos = load_consumer_offset()
    print(f"\n[Consumer] Resuming from offset: {current_pos} (mode: {mode})")
    records = log.read_from(current_pos)
    
    processed = []
    for off, data in records:
        if mode == "commit_before":
            save_consumer_offset(off + 1)
        
        if crash_at is not None and off == crash_at:
            print(f" [CRASH!] Consumer crashed while processing offset {off}!")
            return processed, False
        
        # Simulate business logic
        payload = data.decode()
        processed.append((off, payload))
        print(f" [Process] Offset {off}: {payload}")
        
        if mode == "commit_after":
            save_consumer_offset(off + 1)
            
    return processed, True

if __name__ == "__main__":
    log_path = "/tmp/offsets_demo.dat"
    if os.path.exists(log_path): os.remove(log_path)
    if os.path.exists(OFFSET_STORE): os.remove(OFFSET_STORE)

    log = MiniLog(log_path)
    for i in range(5):
        log.append(f"event-{i}".encode())

    print("--- 1. Crash with 'commit_before' (Risk: Data Loss) ---")
    simulate_consumer(log, mode="commit_before", crash_at=2)
    print("Restarting consumer after crash...")
    simulate_consumer(log, mode="commit_before")

    print("\n--- Resetting State ---")
    if os.path.exists(OFFSET_STORE): os.remove(OFFSET_STORE)

    print("--- 2. Crash with 'commit_after' (Risk: Duplicate Processing) ---")
    simulate_consumer(log, mode="commit_after", crash_at=2)
    print("Restarting consumer after crash...")
    simulate_consumer(log, mode="commit_after")
