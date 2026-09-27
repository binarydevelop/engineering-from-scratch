#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = "/tmp/delivery_lab.db"

def setup_db():
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE orders (id TEXT, amount REAL)")
    conn.commit()
    conn.close()

def at_most_once_flow(events, crash_at=2):
    print("--- Testing AT-MOST-ONCE (Commit BEFORE Processing) ---")
    setup_db()
    committed_offset = 0
    
    for offset, event in enumerate(events):
        # 1. Commit offset FIRST
        committed_offset = offset + 1
        
        # 2. Crash simulation
        if offset == crash_at:
            print(f" [CRASH] Worker killed at offset {offset} BEFORE DB write!")
            break
            
        # 3. DB write
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orders VALUES (?, ?)", (event["id"], event["amount"]))
        conn.commit()
        conn.close()

    print(f"State on disk: Committed offset = {committed_offset}")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT count(*) FROM orders").fetchone()[0]
    print(f"Orders in database: {rows} (Expected {len(events)}) -> DATA LOSS OCCURRED!")
    conn.close()

def at_least_once_flow(events, crash_at=2):
    print("\n--- Testing AT-LEAST-ONCE (Process BEFORE Commit) ---")
    setup_db()
    committed_offset = 0
    
    for offset, event in enumerate(events):
        # 1. DB write FIRST
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orders VALUES (?, ?)", (event["id"], event["amount"]))
        conn.commit()
        conn.close()
        
        # 2. Crash simulation
        if offset == crash_at:
            print(f" [CRASH] Worker killed at offset {offset} AFTER DB write, BEFORE commit!")
            break
            
        # 3. Commit offset SECOND
        committed_offset = offset + 1

    print(f"State on disk: Committed offset = {committed_offset}")
    print("Worker restarts from committed offset and re-processes...")
    # Re-run from committed_offset
    for offset in range(committed_offset, crash_at + 1):
        event = events[offset]
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orders VALUES (?, ?)", (event["id"], event["amount"]))
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT count(*) FROM orders").fetchone()[0]
    print(f"Orders in database: {rows} (Events were 3) -> DUPLICATE PROCESSING OCCURRED!")
    conn.close()

if __name__ == "__main__":
    sample_events = [
        {"id": "ORD-1", "amount": 10.0},
        {"id": "ORD-2", "amount": 20.0},
        {"id": "ORD-3", "amount": 30.0},
    ]
    at_most_once_flow(sample_events, crash_at=1)
    at_least_once_flow(sample_events, crash_at=1)
