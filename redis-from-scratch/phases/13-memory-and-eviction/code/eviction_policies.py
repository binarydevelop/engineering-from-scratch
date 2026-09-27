#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def test_eviction_mechanics():
    print("Testing maxmemory configuration inspection:")
    maxmem = redis_cmd("CONFIG", "GET", "maxmemory")
    policy = redis_cmd("CONFIG", "GET", "maxmemory-policy")
    print(f"Current Config:\n  {maxmem}\n  {policy}")
    print("\nEviction Policies Summary:")
    print("  • noeviction   : Returns error on writes when full. Safe for primary databases.")
    print("  • allkeys-lru  : Evicts least-recently-used keys across entire keyspace. Best for pure caches.")
    print("  • volatile-lru : Evicts least-recently-used keys ONLY among keys with TTLs.")
    print("  • allkeys-lfu  : Evicts least-frequently-used keys. Protects frequently accessed hot keys.")

if __name__ == "__main__":
    try: test_eviction_mechanics()
    except Exception as e: print("Redis offline:", e)
