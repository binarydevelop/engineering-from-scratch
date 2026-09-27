"""
Lesson 02: Build a TCP Server from First Principles.
Uses Python's standard library socket API to demonstrate TCP connection lifecycle:
socket -> bind -> listen -> accept -> recv -> sendall -> close.
"""

import socket
import threading
from typing import Tuple

class SimpleTCPServer:
    """A minimal multi-threaded TCP server using BSD socket APIs."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.port = port
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False
        self._thread: threading.Thread | None = None

    def start(self) -> int:
        """Binds and listens on socket, returning the allocated port."""
        self.sock.bind((self.host, self.port))
        self.port = self.sock.getsockname()[1]
        self.sock.listen(128)
        self.is_running = True
        self._thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._thread.start()
        return self.port

    def _accept_loop(self):
        while self.is_running:
            try:
                conn, addr = self.sock.accept()
                threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
            except OSError:
                break

    def _handle_client(self, conn: socket.socket, addr: Tuple[str, int]):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break  # Client closed connection (FIN packet received)
                # Echo protocol: respond with prefix
                response = b"ECHO:" + data
                conn.sendall(response)

    def stop(self):
        """Shuts down the server socket."""
        self.is_running = False
        try:
            self.sock.close()
        except OSError:
            pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

def main():
    server = SimpleTCPServer()
    port = server.start()
    print(f"TCP Echo Server listening on 127.0.0.1:{port}")
    try:
        import time
        time.sleep(1)
    finally:
        server.stop()

if __name__ == "__main__":
    main()
