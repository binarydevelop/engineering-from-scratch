"""
Lesson 03: Build a Minimal HTTP Server from First Principles.
Parses RFC 9112 HTTP/1.1 byte streams directly over BSD sockets without external frameworks.
"""

import socket
import threading
from typing import Tuple, Dict

class MinimalHTTPServer:
    """A from-scratch HTTP/1.1 server parsing raw CRLF wire protocols."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False
        self._thread: threading.Thread | None = None

    def start(self) -> int:
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
                threading.Thread(target=self._handle_request, args=(conn, addr), daemon=True).start()
            except OSError:
                break

    def _handle_request(self, conn: socket.socket, addr: Tuple[str, int]):
        with conn:
            raw_data = b""
            while b"\r\n\r\n" not in raw_data:
                chunk = conn.recv(1024)
                if not chunk:
                    return
                raw_data += chunk

            header_bytes, body_bytes = raw_data.split(b"\r\n\r\n", 1)
            lines = header_bytes.decode("utf-8").split("\r\n")
            if not lines:
                return

            request_line = lines[0]
            parts = request_line.split(" ")
            if len(parts) != 3:
                response = b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n"
                conn.sendall(response)
                return

            method, path, version = parts
            headers: Dict[str, str] = {}
            for line in lines[1:]:
                if ": " in line:
                    k, v = line.split(": ", 1)
                    headers[k.lower()] = v

            # Dispatch simple responses
            if method == "GET" and path == "/hello":
                body = b"hello from first principles"
                resp = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode("utf-8") + body
            elif method == "GET" and path == "/json":
                body = b'{"status": "ok", "server": "first-principles"}'
                resp = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode("utf-8") + body
            else:
                body = b"Not Found"
                resp = (
                    f"HTTP/1.1 404 Not Found\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode("utf-8") + body

            conn.sendall(resp)

    def stop(self):
        self.is_running = False
        try:
            self.sock.close()
        except OSError:
            pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
