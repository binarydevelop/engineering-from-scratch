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

def test_rdb_snapshot():
    print("Triggering background RDB snapshot (BGSAVE)...")
    res = redis_cmd("BGSAVE")
    print("  BGSAVE Trigger Status:", res)
    time.sleep(1.0)
    info = redis_cmd("INFO", "persistence")
    for line in info.split("\r\n"):
        if any(k in line for k in ["rdb_last_bgsave_status", "rdb_changes_since_last_save", "rdb_last_save_time"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: test_rdb_snapshot()
    except Exception as e: print("Redis offline:", e)
