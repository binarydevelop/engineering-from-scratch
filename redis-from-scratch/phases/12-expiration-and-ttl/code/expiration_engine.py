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

def run_ttl_experiments():
    key = "session:temp_token"
    redis_cmd("SET", key, "user_abc", "EX", "2") # 2 seconds TTL
    print("Initial TTL (seconds):", redis_cmd("TTL", key))
    time.sleep(1.0)
    print("TTL after 1 second:", redis_cmd("TTL", key))
    time.sleep(1.2)
    print("TTL after 2.2 seconds (expired):", redis_cmd("TTL", key))
    print("GET on expired key (triggers passive deletion):", redis_cmd("GET", key))

if __name__ == "__main__":
    try: run_ttl_experiments()
    except Exception as e: print("Redis offline:", e)
