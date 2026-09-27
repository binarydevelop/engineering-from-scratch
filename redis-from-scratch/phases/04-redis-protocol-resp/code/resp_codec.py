#!/usr/bin/env python3
import socket

def encode_resp_command(*args) -> bytes:
    """Encodes command arguments into RESP array."""
    out = [f"*{len(args)}\r\n".encode()]
    for arg in args:
        b = str(arg).encode("utf-8")
        out.append(f"${len(b)}\r\n".encode() + b + b"\r\n")
    return b"".join(out)

def decode_resp(data: bytes):
    """Simple parser for basic RESP response types."""
    if not data: return None
    prefix = chr(data[0])
    payload = data[1:].split(b"\r\n", 1)[0]
    if prefix == "+": return ("SimpleString", payload.decode())
    elif prefix == "-": return ("Error", payload.decode())
    elif prefix == ":": return ("Integer", int(payload))
    elif prefix == "$":
        length = int(payload)
        if length == -1: return ("Null", None)
        val = data.split(b"\r\n", 2)[1]
        return ("BulkString", val.decode(errors="replace"))
    return ("Raw", data)

if __name__ == "__main__":
    cmd = encode_resp_command("SET", "protocol_test", "hello_resp")
    print(f"Encoded RESP bytes for SET protocol_test hello_resp:\n{cmd!r}")
    
    try:
        s = socket.create_connection(("localhost", 6379), timeout=2.0)
        s.sendall(cmd)
        resp = s.recv(1024)
        print(f"Raw response from Redis: {resp!r}")
        print("Decoded response:", decode_resp(resp))
        s.close()
    except Exception as e:
        print("Redis server not reachable, decoded mock response:", decode_resp(b"+OK\r\n"))
