#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_hash_experiments():
    key = "user:1001"
    redis_cmd("DEL", key)
    print("1. Setting hash fields:")
    redis_cmd("HSET", key, "name", "Alice", "email", "alice@example.com", "visits", "0")
    print("  HGET user:1001 name ->", redis_cmd("HGET", key, "name"))
    
    print("\n2. Atomic Field Increments:")
    print("  HINCRBY user:1001 visits 1 ->", redis_cmd("HINCRBY", key, "visits", "1"))
    print("  HINCRBY user:1001 visits 5 ->", redis_cmd("HINCRBY", key, "visits", "5"))

    print("\n3. Field Inspection & Memory Encoding:")
    print("  OBJECT ENCODING user:1001 ->", redis_cmd("OBJECT", "ENCODING", key))
    print("  HGETALL user:1001 ->\n", redis_cmd("HGETALL", key))

if __name__ == "__main__":
    try: run_hash_experiments()
    except Exception as e: print("Redis offline:", e)
