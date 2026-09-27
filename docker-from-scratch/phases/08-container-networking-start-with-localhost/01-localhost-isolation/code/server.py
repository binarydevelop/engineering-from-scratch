#!/usr/bin/env python3
"""
server.py
HTTP server that identifies whether it is running on the host or in a container.
"""

import http.server
import json
import socket
import sys

PORT = 8080

class HostInfoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        client_addr = self.client_address[0]
        
        payload = {
            "message": "Hello from server process",
            "hostname": hostname,
            "client_ip": client_addr,
            "listening_port": PORT,
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
    print(f"[Host Server] Starting on 0.0.0.0:{PORT}...")
    server = http.server.HTTPServer(("0.0.0.0", PORT), HostInfoHandler)
    server.serve_forever()
