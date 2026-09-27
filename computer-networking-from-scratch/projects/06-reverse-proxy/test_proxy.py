#!/usr/bin/env python3
"""
projects/06-reverse-proxy/test_proxy.py
Automated test suite verifying the reverse proxy and round-robin load distribution.
"""

import os
import socket
import sys
import threading
import time
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from reverse_proxy import ReverseProxy


class MockEchoServer:
    def __init__(self, port: int, response_text: str):
        self.port = port
        self.response_text = response_text
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", self.port))
        self.sock.listen(16)
        self.running = True

    def run(self):
        try:
            while self.running:
                conn, _ = self.sock.accept()
                with conn:
                    data = conn.recv(4096)
                    body = self.response_text.encode()
                    resp = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: text/plain\r\n"
                        f"Content-Length: {len(body)}\r\n"
                        f"Connection: close\r\n\r\n"
                    ).encode() + body
                    conn.sendall(resp)
        except Exception:
            pass

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass


class TestReverseProxy(unittest.TestCase):
    def setUp(self):
        # Start 2 backend servers
        self.backend1 = MockEchoServer(9101, "RESPONSE_FROM_BACKEND_1")
        self.backend2 = MockEchoServer(9102, "RESPONSE_FROM_BACKEND_2")
        self.t1 = threading.Thread(target=self.backend1.run, daemon=True)
        self.t2 = threading.Thread(target=self.backend2.run, daemon=True)
        self.t1.start()
        self.t2.start()

        # Start Proxy on 9100 pointing to 9101 and 9102
        self.proxy = ReverseProxy(
            host="127.0.0.1",
            port=9100,
            backends=[("127.0.0.1", 9101), ("127.0.0.1", 9102)],
        )
        self.proxy_thread = threading.Thread(target=self.proxy.run, daemon=True)
        self.proxy_thread.start()
        time.sleep(0.1)

    def tearDown(self):
        self.proxy.close()
        self.backend1.close()
        self.backend2.close()
        time.sleep(0.05)

    def test_round_robin_distribution(self):
        # Request 1 -> Backend 1
        with socket.create_connection(("127.0.0.1", 9100), timeout=1.0) as s:
            s.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n")
            res1 = s.recv(4096).decode()
            self.assertIn("RESPONSE_FROM_BACKEND_1", res1)

        # Request 2 -> Backend 2
        with socket.create_connection(("127.0.0.1", 9100), timeout=1.0) as s:
            s.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n")
            res2 = s.recv(4096).decode()
            self.assertIn("RESPONSE_FROM_BACKEND_2", res2)

    def test_health_check_failover(self):
        # Kill backend 1
        self.backend1.close()
        self.proxy.check_health_once()

        # Both requests should now route to healthy backend 2
        with socket.create_connection(("127.0.0.1", 9100), timeout=1.0) as s:
            s.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n")
            res = s.recv(4096).decode()
            self.assertIn("RESPONSE_FROM_BACKEND_2", res)


if __name__ == "__main__":
    unittest.main()
