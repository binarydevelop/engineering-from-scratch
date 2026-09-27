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

def atomic_fixed_window(user_id, limit=3, window_sec=2):
    now_window = int(time.time() // window_sec)
    key = f"rate:{user_id}:{now_window}"
    raw = redis_cmd("INCR", key)
    count = int(raw.split("\r\n")[0][1:])
    if count == 1:
        redis_cmd("EXPIRE", key, str(window_sec * 2))
    return count <= limit, count

if __name__ == "__main__":
    try:
        print("Testing Atomic Rate Limiter (Limit: 3 requests per 2-second window):")
        for i in range(1, 6):
            allowed, count = atomic_fixed_window("user_42", limit=3, window_sec=2)
            status = "✓ ALLOWED" if allowed else "✗ 429 TOO MANY REQUESTS"
            print(f"  Request #{i}: {status} (Count: {count})")
    except Exception as e: print("Redis offline:", e)
