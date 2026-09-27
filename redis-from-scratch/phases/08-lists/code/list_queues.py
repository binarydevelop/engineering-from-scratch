#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_list_experiments():
    key = "queue:jobs"
    redis_cmd("DEL", key)
    print("1. FIFO Queue (LPUSH -> RPOP):")
    redis_cmd("LPUSH", key, "job_1", "job_2", "job_3")
    print("  Pop first out (RPOP) ->", redis_cmd("RPOP", key))
    print("  Pop next out (RPOP)  ->", redis_cmd("RPOP", key))

    print("\n2. Capped Activity Log (LTRIM):")
    log_key = "user:recent_actions"
    redis_cmd("DEL", log_key)
    for i in range(1, 15):
        redis_cmd("LPUSH", log_key, f"action_{i}")
        redis_cmd("LTRIM", log_key, "0", "4") # Keep only latest 5
    print("  LRANGE 0 -1 (latest 5 actions) ->\n", redis_cmd("LRANGE", log_key, "0", "-1"))

if __name__ == "__main__":
    try: run_list_experiments()
    except Exception as e: print("Redis offline:", e)
