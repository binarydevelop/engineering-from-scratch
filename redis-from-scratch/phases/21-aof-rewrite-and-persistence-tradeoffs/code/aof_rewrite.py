#!/usr/bin/env python3
import socket
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=5.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_aof_rewrite_demo():
    print("Simulating 1,000 increments to generate command history...")
    for _ in range(1000):
        redis_cmd("INCR", "test:rewrite_counter")
    
    print("Triggering background AOF rewrite (BGREWRITEAOF)...")
    res = redis_cmd("BGREWRITEAOF")
    print("  BGREWRITEAOF status:", res)
    time.sleep(1.0)
    info = redis_cmd("INFO", "persistence")
    for line in info.split("\r\n"):
        if any(k in line for k in ["aof_rewrite_in_progress", "aof_last_bgrewrite_status", "aof_current_size", "aof_base_size"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: run_aof_rewrite_demo()
    except Exception as e: print("Redis offline:", e)
