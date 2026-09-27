#!/usr/bin/env python3
"""
projects/02-http-server/test_http.py
Automated test suite verifying the scratch HTTP/1.1 server over raw TCP.
"""

import os
import socket
import sys
import threading
import time
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from http_server import HTTPServer


class TestHTTPServer(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(host="127.0.0.1", port=8099)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        time.sleep(0.1)

    def tearDown(self):
        self.server.close()
        time.sleep(0.05)

    def test_http_get_200(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", 8099))
            req = "GET /api/status HTTP/1.1\r\nHost: 127.0.0.1:8099\r\nConnection: close\r\n\r\n"
            sock.sendall(req.encode())

            res = sock.recv(4096).decode()
            self.assertIn("HTTP/1.1 200 OK", res)
            self.assertIn("Content-Type: application/json", res)
            self.assertIn('"status": "UP"', res)

    def test_http_post_echo(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", 8099))
            body = "binary-data-stream-456"
            req = (
                f"POST /api/echo HTTP/1.1\r\n"
                f"Host: 127.0.0.1:8099\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
                f"{body}"
            )
            sock.sendall(req.encode())

            res = sock.recv(4096).decode()
            self.assertIn("HTTP/1.1 201 Created", res)
            self.assertIn(body, res)

    def test_http_404_not_found(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", 8099))
            req = "GET /random/does/not/exist HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n"
            sock.sendall(req.encode())

            res = sock.recv(4096).decode()
            self.assertIn("HTTP/1.1 404 Not Found", res)


if __name__ == "__main__":
    unittest.main()
