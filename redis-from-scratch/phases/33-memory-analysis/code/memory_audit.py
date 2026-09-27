#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_memory_audit():
    key = "mem:test_overhead"
    redis_cmd("SET", key, "x")
    usage = redis_cmd("MEMORY", "USAGE", key)
    print(f"Key '{key}' with 1-byte value 'x':")
    print(f"  Actual string data : 1 byte")
    print(f"  Redis MEMORY USAGE : {usage} bytes! (~50x overhead for tiny keys)")

    print("\nInspecting Server Memory Metrics (INFO memory):")
    info = redis_cmd("INFO", "memory")
    for line in info.split("\r\n"):
        if any(k in line for k in ["used_memory_human", "used_memory_rss_human", "mem_fragmentation_ratio", "mem_allocator"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: run_memory_audit()
    except Exception as e: print("Redis offline:", e)
