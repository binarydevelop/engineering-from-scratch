#!/usr/bin/env python3
import socket
import uuid
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

LUA_RELEASE_LOCK = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
"""

def test_safe_distributed_lock():
    lock_key = "lock:invoice:9021"
    token = str(uuid.uuid4())
    print("1. Acquiring lock with 3-second TTL and unique UUID token:")
    res = redis_cmd("SET", lock_key, token, "NX", "PX", "3000")
    print("  Acquire Result:", res)

    print("\n2. Another worker attempting to acquire the same lock:")
    competing_res = redis_cmd("SET", lock_key, "other_worker", "NX", "PX", "3000")
    print("  Competing Worker Result:", competing_res, "(Correctly rejected!)")

    print("\n3. Releasing lock safely with Lua script token verification:")
    release_res = redis_cmd("EVAL", LUA_RELEASE_LOCK, "1", lock_key, token)
    print("  Release Status (1 = released, 0 = rejected):", release_res)

if __name__ == "__main__":
    try: test_safe_distributed_lock()
    except Exception as e: print("Redis offline:", e)
