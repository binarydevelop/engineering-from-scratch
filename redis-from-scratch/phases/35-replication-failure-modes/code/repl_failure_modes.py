#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def inspect_replication_backlog():
    print("Inspecting Replication Metrics & Backlog Ring Buffer:")
    info = redis_cmd("INFO", "replication")
    for line in info.split("\r\n"):
        if any(k in line for k in ["role", "connected_slaves", "master_repl_offset", "repl_backlog_active", "repl_backlog_size"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: inspect_replication_backlog()
    except Exception as e: print("Redis offline:", e)
