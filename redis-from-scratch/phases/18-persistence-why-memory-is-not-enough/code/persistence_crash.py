#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_durability_analysis():
    print("Inspecting Current Redis Persistence Configuration:")
    rdb_save = redis_cmd("CONFIG", "GET", "save")
    aof_enabled = redis_cmd("CONFIG", "GET", "appendonly")
    print(f"  RDB Save rules: {rdb_save}")
    print(f"  AOF AppendOnly: {aof_enabled}")
    print("\nSystem Design Durability Spectrum:")
    print("  1. No Persistence : Maximum throughput. Pure ephemeral cache. 100% loss on crash.")
    print("  2. RDB Snapshots  : Low I/O overhead. Point-in-time backup. Loses data since last snapshot.")
    print("  3. AOF (everysec) : Default standard. High durability. Loses at most ~1-2 seconds of writes.")
    print("  4. AOF (always)   : Highest durability (fsync per write). Major throughput penalty.")

if __name__ == "__main__":
    try: run_durability_analysis()
    except Exception as e: print("Redis offline:", e)
