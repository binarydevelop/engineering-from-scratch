#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def test_encoding_transitions():
    key = "demo:encoding_shift"
    redis_cmd("DEL", key)
    
    # Small hash -> listpack
    redis_cmd("HSET", key, "f1", "short_val")
    enc1 = redis_cmd("OBJECT", "ENCODING", key)
    mem1 = redis_cmd("MEMORY", "USAGE", key)
    print(f"Small Hash (f1: 9 bytes) -> Encoding: {enc1}, Memory: {mem1} bytes")

    # Insert giant value (> 64 bytes) -> triggers shift to hashtable
    redis_cmd("HSET", key, "f2", "x" * 128)
    enc2 = redis_cmd("OBJECT", "ENCODING", key)
    mem2 = redis_cmd("MEMORY", "USAGE", key)
    print(f"After inserting 128-byte field -> Encoding: {enc2}, Memory: {mem2} bytes")

if __name__ == "__main__":
    try: test_encoding_transitions()
    except Exception as e: print("Redis offline:", e)
