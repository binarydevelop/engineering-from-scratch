#!/usr/bin/env python3
"""
test_connections.py
Tests TCP socket connections to Redis and Postgres services by hostname.
"""

import socket
import sys

def test_tcp_socket(host: str, port: int):
    print(f"Connecting to {host}:{port}...")
    s = socket.socket(socket.AF_UNIX if host.startswith("/") else socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((host, port))
        print(f"  [SUCCESS] TCP connection established with {host}:{port}!")
        s.close()
        return True
    except Exception as e:
        print(f"  [FAILURE] Could not connect to {host}:{port}: {e}")
        s.close()
        return False

if __name__ == "__main__":
    target_host = sys.argv[1] if len(sys.argv) > 1 else "redis"
    target_port = int(sys.argv[2]) if len(sys.argv) > 2 else 6379
    success = test_tcp_socket(target_host, target_port)
    sys.exit(0 if success else 1)
