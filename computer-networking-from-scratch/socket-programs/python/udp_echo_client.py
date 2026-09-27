#!/usr/bin/env python3
"""
socket-programs/python/udp_echo_client.py
A clean UDP client sending datagrams and timing round-trip delays.
Demonstrates:
  - socket(AF_INET, SOCK_DGRAM)
  - settimeout(seconds) to handle lost datagrams
  - sendto(data, server_address)
  - recvfrom(buffer_size)
"""

import socket
import sys
import time

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999
TIMEOUT_SEC = 2.0


def send_udp_message(message: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT_SEC)
        data = message.encode("utf-8")
        server_addr = (host, port)

        t_start = time.perf_counter()
        sock.sendto(data, server_addr)

        try:
            reply_bytes, addr = sock.recvfrom(4096)
            t_end = time.perf_counter()
            rtt_ms = (t_end - t_start) * 1000.0
            reply = reply_bytes.decode("utf-8", errors="replace")
            print(f"Reply from {addr} in {rtt_ms:.3f} ms: {reply!r}")
            return reply
        except socket.timeout:
            print(f"ERROR: UDP request to {server_addr} timed out after {TIMEOUT_SEC}s (Datagram lost)")
            raise


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello over UDP!"
    h = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_HOST
    p = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_PORT
    send_udp_message(msg, h, p)
