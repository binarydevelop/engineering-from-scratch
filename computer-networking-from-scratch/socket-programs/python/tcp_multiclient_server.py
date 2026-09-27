#!/usr/bin/env python3
"""
socket-programs/python/tcp_multiclient_server.py
A concurrent, single-threaded TCP server using select() I/O multiplexing.
Handles hundreds of simultaneous client connections on a single thread without blocking.
"""

import select
import socket
import sys
from typing import Dict, List

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8889


def run_multiclient_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind((host, port))
    server.listen(128)

    print(f"Multi-Client Event-Loop Server listening on {host}:{port}")

    # Sockets from which we expect to read
    inputs: List[socket.socket] = [server]
    # Sockets to which we expect to write
    outputs: List[socket.socket] = []
    # Outgoing message queues (socket -> bytearray)
    message_queues: Dict[socket.socket, bytearray] = {}

    try:
        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs, 1.0)

            # 1. Handle readable sockets
            for s in readable:
                if s is server:
                    # A 'readable' server socket is ready to accept a new connection
                    conn, client_addr = s.accept()
                    conn.setblocking(False)
                    inputs.append(conn)
                    message_queues[conn] = bytearray()
                    print(f"[+] New client connected from {client_addr} (Total clients: {len(inputs)-1})")
                else:
                    # Client socket has sent data
                    try:
                        data = s.recv(4096)
                        if data:
                            # Echo data back
                            message_queues[s].extend(data)
                            if s not in outputs:
                                outputs.append(s)
                        else:
                            # Empty read means client closed connection (EOF)
                            print(f"[-] Client disconnected: {s.getpeername()}")
                            if s in outputs:
                                outputs.remove(s)
                            inputs.remove(s)
                            s.close()
                            del message_queues[s]
                    except ConnectionResetError:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]

            # 2. Handle writable sockets
            for s in writable:
                if s in message_queues and message_queues[s]:
                    try:
                        sent = s.send(message_queues[s])
                        message_queues[s] = message_queues[s][sent:]
                    except BlockingIOError:
                        pass
                if s in message_queues and len(message_queues[s]) == 0:
                    outputs.remove(s)

            # 3. Handle exceptional sockets
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                if s in message_queues:
                    del message_queues[s]

    except KeyboardInterrupt:
        print("\nShutting down multi-client server...")
    finally:
        for s in inputs:
            s.close()


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    p = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    run_multiclient_server(h, p)
