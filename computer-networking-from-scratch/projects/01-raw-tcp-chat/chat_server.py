#!/usr/bin/env python3
"""
projects/01-raw-tcp-chat/chat_server.py
Multi-user conversational chat server built from scratch using raw POSIX sockets and select().
Broadcasts messages between all connected chat participants.
"""

import select
import socket
import sys
from typing import Dict, List

DEFAULT_PORT = 9001


class ChatServer:
    def __init__(self, host: str = "127.0.0.1", port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(64)
        self.server_sock.setblocking(False)

        self.sockets: List[socket.socket] = [self.server_sock]
        self.clients: Dict[socket.socket, str] = {}  # socket -> nickname
        self.running = True

    def broadcast(self, sender_sock: socket.socket, message: str) -> None:
        """Sends message to all clients except the sender."""
        msg_bytes = message.encode("utf-8")
        for s in list(self.clients.keys()):
            if s != sender_sock:
                try:
                    s.sendall(msg_bytes)
                except Exception:
                    self.remove_client(s)

    def remove_client(self, client_sock: socket.socket) -> None:
        """Cleans up disconnected client."""
        if client_sock in self.clients:
            nick = self.clients[client_sock]
            del self.clients[client_sock]
            if client_sock in self.sockets:
                self.sockets.remove(client_sock)
            try:
                client_sock.close()
            except Exception:
                pass
            print(f"[-] {nick} left the chat.")
            self.broadcast(client_sock, f"*** {nick} has left the chat ***\n")

    def run_step(self, timeout: float = 0.5) -> None:
        """Executes a single event-loop step (useful for testing and non-blocking operation)."""
        readable, _, _ = select.select(self.sockets, [], [], timeout)
        for s in readable:
            if s is self.server_sock:
                conn, addr = self.server_sock.accept()
                conn.setblocking(False)
                self.sockets.append(conn)
                nick = f"User_{addr[1]}"
                self.clients[conn] = nick
                print(f"[+] {nick} joined from {addr}")
                conn.sendall(f"*** Welcome to the Chat, {nick}! ***\n".encode("utf-8"))
                self.broadcast(conn, f"*** {nick} has joined the chat ***\n")
            else:
                try:
                    data = s.recv(4096)
                    if data:
                        text = data.decode("utf-8", errors="replace").strip()
                        sender_nick = self.clients.get(s, "Unknown")
                        msg = f"[{sender_nick}] {text}\n"
                        print(f"Chat: {msg.strip()}")
                        self.broadcast(s, msg)
                    else:
                        self.remove_client(s)
                except ConnectionResetError:
                    self.remove_client(s)

    def run(self) -> None:
        print(f"Chat Server running on {self.host}:{self.port}")
        try:
            while self.running:
                self.run_step(timeout=1.0)
        except KeyboardInterrupt:
            print("\nShutting down chat server.")
        finally:
            self.close()

    def close(self) -> None:
        self.running = False
        for s in self.sockets:
            s.close()


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    server = ChatServer(port=p)
    server.run()
