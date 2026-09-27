#!/usr/bin/env python3
"""
app.py
HTTP service listening on container port 8000.
Demonstrates port binding, EXPOSE documentation, and host port forwarding.
"""

import http.server
import json
import socket
import sys

PORT = 8000

class PortDemoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {
            "status": "connected",
            "container_hostname": socket.gethostname(),
            "container_internal_port": PORT,
            "client_address": self.client_address[0],
            "client_port": self.client_address[1],
        }
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print(f"Server listening internally on 0.0.0.0:{PORT}...")
    server = http.server.HTTPServer(("0.0.0.0", PORT), PortDemoHandler)
    server.serve_forever()
