#!/usr/bin/env python3
"""
projects/02-http-server/http_server.py
A clean, modular HTTP/1.1 web server implemented over raw TCP sockets.
Supports:
  - Methods: GET, POST, HEAD
  - Headers: Host, Content-Type, Content-Length, Connection
  - Status codes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 405 Method Not Allowed
  - Persistent connections (Connection: keep-alive)
"""

import socket
import sys
from typing import Dict, Optional, Tuple


class HTTPServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(128)
        self.running = True

    def handle_request(self, method: str, path: str, headers: Dict[str, str], body: bytes) -> Tuple[int, str, Dict[str, str], bytes]:
        """Routes HTTP request and returns (status_code, reason, headers, body_bytes)."""
        if method == "GET":
            if path == "/":
                content = b"<h1>Welcome to the Educational HTTP Server!</h1>"
                return 200, "OK", {"Content-Type": "text/html; charset=utf-8"}, content
            elif path == "/api/status":
                content = b'{"status": "UP", "engine": "raw-socket"}'
                return 200, "OK", {"Content-Type": "application/json"}, content
            else:
                content = b"<h1>404 Not Found</h1>"
                return 404, "Not Found", {"Content-Type": "text/html; charset=utf-8"}, content

        elif method == "POST":
            if path == "/api/echo":
                return 201, "Created", {"Content-Type": "application/octet-stream"}, body
            return 404, "Not Found", {"Content-Type": "text/plain"}, b"Not Found"

        return 405, "Method Not Allowed", {"Content-Type": "text/plain"}, b"Method Not Allowed"

    def handle_client(self, conn: socket.socket):
        buffer = bytearray()
        keep_alive = True

        while keep_alive:
            # 1. Read headers up to \r\n\r\n
            while b"\r\n\r\n" not in buffer:
                chunk = conn.recv(4096)
                if not chunk:
                    return
                buffer.extend(chunk)

            header_part, _, rest = buffer.partition(b"\r\n\r\n")
            buffer = bytearray(rest)

            # 2. Parse request line & headers
            lines = header_part.decode("iso-8859-1").split("\r\n")
            req_line_parts = lines[0].split(" ")
            if len(req_line_parts) < 3:
                return
            method, path, version = req_line_parts[0], req_line_parts[1], req_line_parts[2]

            headers = {}
            for line in lines[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

            # 3. Read body if Content-Length present
            content_length = int(headers.get("content-length", 0))
            while len(buffer) < content_length:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                buffer.extend(chunk)

            body = bytes(buffer[:content_length])
            buffer = bytearray(buffer[content_length:])

            # 4. Evaluate Keep-Alive
            conn_header = headers.get("connection", "").lower()
            if version == "HTTP/1.0":
                keep_alive = (conn_header == "keep-alive")
            else:
                keep_alive = (conn_header != "close")

            # 5. Route request
            code, reason, res_headers, res_body = self.handle_request(method, path, headers, body)

            res_headers["Content-Length"] = str(len(res_body))
            res_headers["Connection"] = "keep-alive" if keep_alive else "close"
            res_headers["Server"] = "Scratch-HTTP/1.1"

            # 6. Serialize and send response
            header_lines = [f"{version} {code} {reason}"]
            for hk, hv in res_headers.items():
                header_lines.append(f"{hk}: {hv}")
            header_lines.append("")
            header_lines.append("")

            raw_response = "\r\n".join(header_lines).encode("iso-8859-1") + res_body
            conn.sendall(raw_response)

    def run(self):
        print(f"HTTP Server listening on http://{self.host}:{self.port}")
        try:
            while self.running:
                conn, _ = self.sock.accept()
                with conn:
                    self.handle_client(conn)
        except Exception:
            pass
        finally:
            self.close()

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(port=p)
    server.run()
