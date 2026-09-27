#!/usr/bin/env python3
import time
import sqlite3
import os

def run_comparison(n=5000):
    print(f"Comparing RAM dictionary vs Disk SQLite over {n:,} read/write operations...")
    # 1. RAM Access
    mem = {}
    t0 = time.perf_counter()
    for i in range(n):
        mem[f"k{i}"] = f"v{i}"
        _ = mem[f"k{i}"]
    ram_time = time.perf_counter() - t0

    # 2. Disk SQLite
    db_file = "/tmp/test_phase01.db"
    if os.path.exists(db_file): os.remove(db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("CREATE TABLE kv (k TEXT PRIMARY KEY, v TEXT);")
    conn.commit()

    t0 = time.perf_counter()
    for i in range(min(n, 1000)): # Capped for test execution speed
        cur.execute("INSERT OR REPLACE INTO kv VALUES (?, ?)", (f"k{i}", f"v{i}"))
        cur.execute("SELECT v FROM kv WHERE k = ?", (f"k{i}",))
        _ = cur.fetchone()
    conn.commit()
    disk_time = time.perf_counter() - t0
    conn.close()
    if os.path.exists(db_file): os.remove(db_file)

    print(f"  • RAM In-Memory Dict: {ram_time:.4f}s  ({(n*2)/ram_time:,.0f} ops/sec)")
    print(f"  • Disk SQLite (WAL) : {disk_time:.4f}s  ({(min(n,1000)*2)/disk_time:,.0f} ops/sec)")
    print(f"  -> RAM is ~{(disk_time/ram_time)*(n/min(n,1000)):.1f}x faster than disk transactions.")

if __name__ == "__main__":
    run_comparison()
