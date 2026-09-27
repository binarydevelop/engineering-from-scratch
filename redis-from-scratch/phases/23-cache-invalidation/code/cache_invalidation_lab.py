#!/usr/bin/env python3
import socket
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_invalidation_demo():
    key = "user:settings:99"
    # Seed cache
    redis_cmd("SET", key, "theme=dark")
    print("1. Initial Cached Setting:", redis_cmd("GET", key))

    # Simulate database update
    print("2. User updates setting in SQL DB to 'theme=light'...")
    # INCORRECT APPROACH: Forget to invalidate cache
    print("  Without invalidation, cache still returns:", redis_cmd("GET", key), "(STALE DATA ANOMALY!)")

    # CORRECT APPROACH: Explicit Cache Invalidation
    print("3. Executing explicit DEL invalidation:")
    redis_cmd("DEL", key)
    print("  Cache key after invalidation ->", redis_cmd("GET", key), "(Next read will fetch from DB)")

if __name__ == "__main__":
    try: run_invalidation_demo()
    except Exception as e: print("Redis offline:", e)
