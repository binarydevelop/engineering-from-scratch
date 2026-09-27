#!/usr/bin/env python3
"""
socket-programs/python/packet_loss_proxy.py
A local UDP proxy that introduces synthetic network unreliability:
  - Packet Loss (drop percentage)
  - Latency / Delay (artificial sleep)
  - Duplication
Enables realistic failure testing without root privileges or kernel modification.
"""

import random
import socket
import sys
import time

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 9998
TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9999


def run_unreliable_proxy(
    loss_rate: float = 0.30,      # 30% packet loss
    delay_ms: float = 50.0,       # 50ms delay
    duplicate_rate: float = 0.10, # 10% packet duplication
):
    proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_sock.bind((LISTEN_HOST, LISTEN_PORT))

    print(f"Unreliable Network Proxy running on {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"Forwarding to target {TARGET_HOST}:{TARGET_PORT}")
    print(f"Loss Rate: {loss_rate*100:.0f}% | Added Delay: {delay_ms:.0f}ms | Duplication: {duplicate_rate*100:.0f}%")

    # Map client address to backend forwarding socket
    while True:
        data, client_addr = proxy_sock.recvfrom(4096)

        # 1. Simulate Packet Loss
        if random.random() < loss_rate:
            print(f"[DROP] Dropped {len(data)} bytes from {client_addr}")
            continue

        # 2. Simulate Latency / Delay
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)

        # 3. Forward to Target
        backend_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        backend_sock.settimeout(2.0)
        backend_sock.sendto(data, (TARGET_HOST, TARGET_PORT))

        # Check for duplication
        if random.random() < duplicate_rate:
            print(f"[DUP] Duplicated packet to target!")
            backend_sock.sendto(data, (TARGET_HOST, TARGET_PORT))

        try:
            reply, _ = backend_sock.recvfrom(4096)
            proxy_sock.sendto(reply, client_addr)
        except socket.timeout:
            pass
        finally:
            backend_sock.close()


if __name__ == "__main__":
    run_unreliable_proxy()
