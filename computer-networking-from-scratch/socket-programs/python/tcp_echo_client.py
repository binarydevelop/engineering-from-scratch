#!/usr/bin/env python3
"""
socket-programs/python/tcp_echo_client.py
A clean TCP client demonstrating connection establishment, ephemeral port binding,
and stream transfer.
Demonstrates:
  - socket(AF_INET, SOCK_STREAM)
  - getsockname() inspecting OS-assigned ephemeral source port
  - connect((host, port)) (3-way handshake)
  - sendall(data)
  - recv(buffer_size)
  - close() (graceful FIN teardown)
"""

import socket
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8888


def send_tcp_message(message: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))

        # Inspect local endpoint allocated by OS kernel
        local_ip, local_port = sock.getsockname()
        print(f"[+] Connected! Kernel allocated Ephemeral Source Port: {local_port} (fd={sock.fileno()})")
        print(f"    4-Tuple: ({local_ip}:{local_port} <-> {host}:{port})")

        payload = message.encode("utf-8")
        sock.sendall(payload)

        # Receive echo
        received = bytearray()
        while len(received) < len(payload):
            chunk = sock.recv(4096)
            if not chunk:
                break
            received.extend(chunk)

        result = received.decode("utf-8", errors="replace")
        print(f"[+] Received Echo: {result!r}")
        return result


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello from TCP Client!"
    h = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_HOST
    p = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_PORT
    send_tcp_message(msg, h, p)
