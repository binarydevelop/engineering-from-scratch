#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def inspect_latency_tools():
    print("1. Inspecting SLOWLOG:")
    slow_len = redis_cmd("SLOWLOG", "LEN")
    print(f"  Total logged slow operations: {slow_len}")
    slow_entries = redis_cmd("SLOWLOG", "GET", "3")
    print(f"  Recent Slow Entries:\n  {slow_entries}")

    print("\n2. Checking Latency Monitor Threshold:")
    thresh = redis_cmd("CONFIG", "GET", "latency-monitor-threshold")
    print(f"  {thresh}")

if __name__ == "__main__":
    try: inspect_latency_tools()
    except Exception as e: print("Redis offline:", e)
