#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_security_inspection():
    print("Inspecting Redis Security Configuration:")
    prot = redis_cmd("CONFIG", "GET", "protected-mode")
    print(f"  Protected Mode: {prot}")
    
    print("\nACL User Principles (Redis 6.0+):")
    print("  Example Production ACL Rule:")
    print("    ACL SETUSER api_read_only on >secretpass ~cache:* +@read -@admin")
    print("    • Only allowed to read keys matching 'cache:*'")
    print("    • Cannot execute administrative commands (FLUSHALL, SHUTDOWN, CONFIG)")

if __name__ == "__main__":
    try: run_security_inspection()
    except Exception as e: print("Redis offline:", e)
