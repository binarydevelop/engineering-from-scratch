#!/usr/bin/env python3
"""
socket-programs/python/tcp_echo_server.py
A robust TCP echo server emphasizing the listening vs connected socket distinction.
Demonstrates:
  - socket(AF_INET, SOCK_STREAM)
  - setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  - bind((host, port))
  - listen(backlog)
  - accept() returning (connected_socket, client_address)
  - recv() stream reading until EOF
"""

import socket
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8888
BACKLOG = 128
BUFFER_SIZE = 4096


def run_tcp_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    # 1. Create listening socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        # Prevent "Address already in use" errors during rapid restart
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. Bind to local interface and port
        listener.bind((host, port))

        # 3. Enter listening passive state
        listener.listen(BACKLOG)
        print(f"TCP Listening Socket bound to {host}:{port} (fd={listener.fileno()})")
        print("Waiting for incoming 3-way handshakes...")

        try:
            while True:
                # 4. Accept incoming connection (creates new connected socket)
                conn, client_addr = listener.accept()
                with conn:
                    print(f"\n[+] Accepted connection from {client_addr} (conn_fd={conn.fileno()})")
                    while True:
                        # 5. Read byte stream
                        chunk = conn.recv(BUFFER_SIZE)
                        if not chunk:
                            print(f"[-] Client {client_addr} closed connection (EOF received)")
                            break
                        print(f"    Received: {chunk.decode('utf-8', errors='replace')!r}")
                        # 6. Echo bytes back
                        conn.sendall(chunk)
        except KeyboardInterrupt:
            print("\nTCP Server stopped.")


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    p = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    run_tcp_server(h, p)
