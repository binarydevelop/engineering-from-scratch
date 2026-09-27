#!/usr/bin/env python3
import http.server
import json
import os
import signal
import sys

PORT = int(os.environ.get("PORT", 8080))
SERVICE_NAME = os.environ.get("SERVICE_NAME", "lfs-api")

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {"status": "ok", "service": SERVICE_NAME, "pid": os.getpid()}
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write(f"[{SERVICE_NAME}] " + format % args + "\n")
        sys.stdout.flush()

def handle_sigterm(signum, frame):
    sys.stdout.write(f"[{SERVICE_NAME}] Caught SIGTERM. Performing graceful shutdown...\n")
    sys.stdout.flush()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

sys.stdout.write(f"[{SERVICE_NAME}] Starting daemon on port {PORT} (PID: {os.getpid()})...\n")
sys.stdout.flush()

with http.server.HTTPServer(("0.0.0.0", PORT), HealthHandler) as httpd:
    httpd.serve_forever()
