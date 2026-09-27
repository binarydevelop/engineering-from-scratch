#!/usr/bin/env python3
import socket
import time
import json

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def simulated_sql_query(user_id):
    # Simulate database disk I/O and query planning delay
    time.sleep(0.02) # 20ms
    return {"id": user_id, "name": f"User_{user_id}", "status": "active"}

def get_user_profile(user_id):
    cache_key = f"user:profile:{user_id}"
    t0 = time.perf_counter()
    
    # 1. Check Redis
    cached = redis_cmd("GET", cache_key)
    if cached and not cached.startswith("$-1"):
        latency_ms = (time.perf_counter() - t0) * 1000
        return json.loads(cached.split("\r\n")[-1]), "CACHE_HIT", latency_ms

    # 2. Cache Miss -> Query Database
    db_data = simulated_sql_query(user_id)
    # 3. Populate Redis Cache with 10s TTL
    redis_cmd("SET", cache_key, json.dumps(db_data), "EX", "10")
    latency_ms = (time.perf_counter() - t0) * 1000
    return db_data, "CACHE_MISS", latency_ms

if __name__ == "__main__":
    try:
        redis_cmd("DEL", "user:profile:42")
        print("1. First Request (Cold Cache):")
        data, status, lat = get_user_profile(42)
        print(f"  Status: {status:10} | Latency: {lat:6.2f} ms | Data: {data}")

        print("\n2. Second Request (Warm Cache):")
        data, status, lat = get_user_profile(42)
        print(f"  Status: {status:10} | Latency: {lat:6.2f} ms | Data: {data}")
    except Exception as e:
        print("Redis offline:", e)
