#!/usr/bin/env python3
"""
socket-programs/python/http_server_raw.py
A clean HTTP/1.1 web server implemented from scratch directly on top of raw POSIX TCP sockets.
Does NOT use http.server or external web frameworks.

Demonstrates:
  - Parsing HTTP request line (Method, Path, Version)
  - Parsing request headers until blank line delimiter (\r\n\r\n)
  - Constructing HTTP responses with correct status lines and headers
  - HTTP Keep-Alive persistent connection handling
"""

import json
import socket
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080


def handle_http_connection(conn: socket.socket, client_addr):
    buffer = bytearray()
    keep_alive = True

    while keep_alive:
        # Read until HTTP header delimiter \r\n\r\n is found
        while b"\r\n\r\n" not in buffer:
            chunk = conn.recv(4096)
            if not chunk:
                return  # Client closed connection
            buffer.extend(chunk)

        header_bytes, _, rest = buffer.partition(b"\r\n\r\n")
        buffer = bytearray(rest)

        # Parse request line & headers
        lines = header_bytes.decode("utf-8", errors="replace").split("\r\n")
        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) < 3:
            return

        method, path, version = parts[0], parts[1], parts[2]
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        # Check Keep-Alive
        conn_header = headers.get("connection", "").lower()
        if version == "HTTP/1.0":
            keep_alive = (conn_header == "keep-alive")
        else:  # HTTP/1.1 default is Keep-Alive
            keep_alive = (conn_header != "close")

        # Routing
        if path == "/":
            body = "<html><body><h1>computer-networking-from-scratch</h1><p>HTTP over raw TCP works!</p></body></html>"
            content_type = "text/html; charset=utf-8"
            status = "200 OK"
        elif path == "/health":
            body = json.dumps({"status": "UP", "protocol": version, "client": str(client_addr)})
            content_type = "application/json"
            status = "200 OK"
        else:
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            content_type = "text/html; charset=utf-8"
            status = "404 Not Found"

        body_bytes = body.encode("utf-8")
        conn_status = "keep-alive" if keep_alive else "close"

        response_headers = (
            f"{version} {status}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            f"Connection: {conn_status}\r\n"
            f"Server: Raw-TCP-Educational-Server/1.0\r\n"
            f"\r\n"
        )

        conn.sendall(response_headers.encode("utf-8") + body_bytes)


def run_http_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((host, port))
        listener.listen(128)
        print(f"Raw TCP HTTP/1.1 Server listening at http://{host}:{port}/")
        print("Endpoints:")
        print("  GET /")
        print("  GET /health")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                conn, addr = listener.accept()
                with conn:
                    handle_http_connection(conn, addr)
        except KeyboardInterrupt:
            print("\nHTTP Server shutting down.")


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    p = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    run_http_server(h, p)
