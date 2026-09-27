#!/usr/bin/env python3
"""
socket-programs/python/udp_echo_server.py
A clean UDP echo server built with standard POSIX socket API.
Demonstrates:
  - socket(AF_INET, SOCK_DGRAM)
  - bind((host, port))
  - recvfrom(buffer_size) returning (data, client_address)
  - sendto(data, client_address)
"""

import socket
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999
BUFFER_SIZE = 4096


def run_udp_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    # 1. Create UDP datagram socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # 2. Bind to host and port
        sock.bind((host, port))
        print(f"UDP Echo Server listening on {host}:{port}")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                # 3. Receive datagram and sender address
                data, client_addr = sock.recvfrom(BUFFER_SIZE)
                message = data.decode("utf-8", errors="replace")
                print(f"Received {len(data)} bytes from {client_addr}: {message!r}")

                # 4. Echo back datagram directly to sender
                sock.sendto(data, client_addr)
        except KeyboardInterrupt:
            print("\nServer shutting down gracefully.")


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    p = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    run_udp_server(h, p)
