#!/usr/bin/env python3
import socket
import sys

def verify_tcp_connection(host="localhost", port=6379):
    print(f"Connecting to Redis at {host}:{port} via raw TCP socket...")
    try:
        s = socket.create_connection((host, port), timeout=2.0)
        # Send raw RESP PING: *1\r\n$4\r\nPING\r\n
        s.sendall(b"*1\r\n$4\r\nPING\r\n")
        response = s.recv(1024)
        s.close()
        print(f"Received raw response bytes: {response!r}")
        if b"+PONG" in response:
            print("✓ SUCCESS: Redis server is healthy and responding to raw RESP PING.")
            return True
        else:
            print(f"✗ UNEXPECTED RESPONSE: {response!r}")
            return False
    except ConnectionRefusedError:
        print(f"✗ ERROR: Connection refused on {host}:{port}. Is redis-server running?")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    ok = verify_tcp_connection()
    sys.exit(0 if ok else 1)
