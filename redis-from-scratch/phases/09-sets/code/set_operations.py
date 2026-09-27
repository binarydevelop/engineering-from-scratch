#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_set_experiments():
    s1 = "skills:alice"
    s2 = "skills:bob"
    redis_cmd("DEL", s1, s2)
    
    redis_cmd("SADD", s1, "python", "docker", "redis", "distributed_systems")
    redis_cmd("SADD", s2, "redis", "linux", "distributed_systems", "kubernetes")

    print("1. Membership Test:")
    print("  Is Alice skilled in 'redis'? ->", redis_cmd("SISMEMBER", s1, "redis"))
    print("  Is Alice skilled in 'rust'?  ->", redis_cmd("SISMEMBER", s1, "rust"))

    print("\n2. Set Algebra (Server-Side Intersections & Unions):")
    print("  Mutual Skills (SINTER Alice Bob):\n", redis_cmd("SINTER", s1, s2))
    print("  Unique Skills of Alice (SDIFF Alice Bob):\n", redis_cmd("SDIFF", s1, s2))

if __name__ == "__main__":
    try: run_set_experiments()
    except Exception as e: print("Redis offline:", e)
