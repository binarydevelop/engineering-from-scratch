#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_streams_demo():
    stream = "stream:telemetry"
    group = "group:analytics"
    redis_cmd("DEL", stream)
    
    # 1. Append entries
    id1 = redis_cmd("XADD", stream, "*", "sensor", "temp", "val", "22.5")
    id2 = redis_cmd("XADD", stream, "*", "sensor", "pressure", "val", "1013")
    print(f"Appended entries to stream:\n  {id1}\n  {id2}")

    # 2. Create Consumer Group
    redis_cmd("XGROUP", "CREATE", stream, group, "0")

    # 3. Worker reads message
    read_res = redis_cmd("XREADGROUP", "GROUP", group, "worker_1", "COUNT", "1", "STREAMS", stream, ">")
    print(f"\nWorker 1 read message:\n  {read_res}")

    # 4. Check Pending Entries List (PEL) before XACK
    pel = redis_cmd("XPENDING", stream, group)
    print(f"\nPEL Status (Pending Acknowledgment):\n  {pel}")

if __name__ == "__main__":
    try: run_streams_demo()
    except Exception as e: print("Redis offline:", e)
