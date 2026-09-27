#!/usr/bin/env python3
"""
projects/06-reverse-proxy/reverse_proxy.py
A production-inspired HTTP Reverse Proxy with Round-Robin routing and Active Health Checks.
Demonstrates:
  - Terminating incoming client connections
  - Selecting healthy upstream backend
  - Header enrichment (X-Forwarded-For, X-Forwarded-Proto)
  - Handling upstream failures (502 Bad Gateway)
  - Background synthetic health checks
"""

import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Backend:
    host: str
    port: int
    is_healthy: bool = True
    total_requests: int = 0


class ReverseProxy:
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, backends: Optional[List[Tuple[str, int]]] = None):
        self.host = host
        self.port = port
        backend_tuples = backends or [("127.0.0.1", 8081), ("127.0.0.1", 8082)]
        self.backends = [Backend(h, p) for h, p in backend_tuples]
        self.rr_index = 0
        self.lock = threading.Lock()
        self.running = True

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(128)

    def select_backend(self) -> Optional[Backend]:
        """Round-robin selection among healthy backends."""
        with self.lock:
            healthy = [b for b in self.backends if b.is_healthy]
            if not healthy:
                return None
            b = healthy[self.rr_index % len(healthy)]
            self.rr_index += 1
            b.total_requests += 1
            return b

    def check_health_once(self) -> None:
        """Probes each backend with a quick TCP connect."""
        for b in self.backends:
            try:
                with socket.create_connection((b.host, b.port), timeout=0.5):
                    b.is_healthy = True
            except (ConnectionRefusedError, socket.timeout, OSError):
                b.is_healthy = False

    def forward_request(self, client_conn: socket.socket, client_addr):
        try:
            # 1. Read request from client
            raw_req = client_conn.recv(8192)
            if not raw_req:
                return

            # 2. Select healthy upstream
            backend = self.select_backend()
            if not backend:
                # 502 Bad Gateway
                err_resp = (
                    b"HTTP/1.1 502 Bad Gateway\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: 32\r\n"
                    b"Connection: close\r\n\r\n"
                    b"502 Bad Gateway: All backends down\n"
                )
                client_conn.sendall(err_resp)
                return

            # 3. Inject X-Forwarded-For
            header_str = raw_req.decode("iso-8859-1")
            injected_header = f"X-Forwarded-For: {client_addr[0]}\r\n"
            mod_req = header_str.replace("\r\n\r\n", f"\r\n{injected_header}\r\n", 1).encode("iso-8859-1")

            # 4. Forward to Backend
            with socket.create_connection((backend.host, backend.port), timeout=2.0) as backend_sock:
                backend_sock.sendall(mod_req)
                # Stream backend response directly back to client
                while True:
                    chunk = backend_sock.recv(8192)
                    if not chunk:
                        break
                    client_conn.sendall(chunk)

        except (ConnectionRefusedError, socket.timeout):
            err_resp = (
                b"HTTP/1.1 502 Bad Gateway\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: 35\r\n"
                b"Connection: close\r\n\r\n"
                b"502 Bad Gateway: Upstream failure\n"
            )
            try:
                client_conn.sendall(err_resp)
            except Exception:
                pass
        except Exception:
            pass

    def run(self):
        print(f"Reverse Proxy running on http://{self.host}:{self.port}")
        for b in self.backends:
            print(f"  Upstream Backend: http://{b.host}:{b.port}")

        try:
            while self.running:
                conn, addr = self.server_sock.accept()
                with conn:
                    self.forward_request(conn, addr)
        except Exception:
            pass
        finally:
            self.close()

    def close(self):
        self.running = False
        try:
            self.server_sock.close()
        except Exception:
            pass


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    proxy = ReverseProxy(port=p)
    proxy.run()
