#!/usr/bin/env python3
"""
app.py
Minimal Python HTTP service for Phase 05 Dockerfile lesson.
"""

import http.server
import json
import os
import sys

PORT = 8000
SERVICE_NAME = os.environ.get("SERVICE_NAME", "unnamed-service")

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {
            "status": "ok",
            "message": "Hello from custom Dockerfile image!",
            "service_name": SERVICE_NAME,
            "cwd": os.getcwd(),
        }
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        sys.stdout.write(f"[{SERVICE_NAME}] " + (format % args) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    print(f"Starting {SERVICE_NAME} on 0.0.0.0:{PORT}...")
    server = http.server.HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    server.serve_forever()
