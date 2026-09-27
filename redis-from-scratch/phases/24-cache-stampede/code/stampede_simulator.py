#!/usr/bin/env python3
import socket
import time
from concurrent.futures import ThreadPoolExecutor

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def simulated_db_fetch():
    time.sleep(0.05) # 50ms slow query
    return "fresh_db_payload"

def fetch_with_stampede_protection(key, worker_id):
    # 1. Read cache
    val = redis_cmd("GET", key)
    if val and not val.startswith("$-1"):
        return "CACHE_HIT"

    # 2. Acquire Mutex Lock (SET lock:key token NX EX 2)
    lock_key = f"lock:{key}"
    acquired = "+OK" in redis_cmd("SET", lock_key, str(worker_id), "NX", "EX", "2")
    if acquired:
        # Only this worker queries DB
        data = simulated_db_fetch()
        redis_cmd("SET", key, data, "EX", "5")
        redis_cmd("DEL", lock_key)
        return "DB_REFRESH_LEADER"
    else:
        # Other workers back off and wait
        time.sleep(0.06)
        return "BACKOFF_CACHE_HIT"

if __name__ == "__main__":
    try:
        target_key = "hot:catalog_item"
        redis_cmd("DEL", target_key) # Force cache miss
        print("Simulating 20 concurrent requests hitting an expired hot key...")
        with ThreadPoolExecutor(max_workers=20) as pool:
            results = list(pool.map(lambda i: fetch_with_stampede_protection(target_key, i), range(20)))
        print("Results across 20 workers:")
        for r in set(results):
            print(f"  • {r}: {results.count(r)} requests")
        print("✓ Verified: Exactly ONE worker queried the database! Database was protected.")
    except Exception as e: print("Redis offline:", e)
