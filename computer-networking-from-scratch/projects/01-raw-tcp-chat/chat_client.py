#!/usr/bin/env python3
"""
projects/01-raw-tcp-chat/chat_client.py
Interactive or scriptable TCP chat client.
"""

import socket
import sys


def run_chat_client(host: str = "127.0.0.1", port: int = 9001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        print(f"Connected to chat server at {host}:{port}")
        # Print welcome banner
        banner = sock.recv(1024).decode("utf-8", errors="replace")
        print(banner, end="")

        while True:
            msg = input("> ")
            if not msg:
                continue
            if msg.lower() in ("/quit", "/exit"):
                break
            sock.sendall((msg + "\n").encode("utf-8"))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("\nDisconnected from chat.")


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 9001
    run_chat_client(h, p)
