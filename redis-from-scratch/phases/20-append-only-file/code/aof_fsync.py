#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def inspect_aof_configuration():
    print("Inspecting AOF Durability Settings:")
    aof_sync = redis_cmd("CONFIG", "GET", "appendfsync")
    print(f"  Current appendfsync: {aof_sync}")
    print("\nUnderstanding fsync System Call:")
    print("  • write() only copies bytes to the OS kernel buffer cache; data is still in RAM!")
    print("  • fsync() forces the OS to physically flush blocks to the storage hardware.")
    print("  • appendfsync everysec uses a background thread to call fsync() once per second,")
    print("    keeping disk I/O off the critical path of the main Redis event loop.")

if __name__ == "__main__":
    try: inspect_aof_configuration()
    except Exception as e: print("Redis offline:", e)
