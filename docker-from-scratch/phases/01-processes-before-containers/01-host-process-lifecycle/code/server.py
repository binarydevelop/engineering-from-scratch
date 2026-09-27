#!/usr/bin/env python3
"""
server.py
A minimal HTTP server that exposes host process properties:
PID, PPID, Environment Variables, Signals, and Exit Codes.
"""

import http.server
import json
import os
import signal
import sys
import time

HOST = "127.0.0.1"
PORT = 8001
RUNNING = True

def handle_sigterm(signum, frame):
    global RUNNING
    sig_name = "SIGTERM" if signum == signal.SIGTERM else "SIGINT"
    sys.stderr.write(f"\n[server.py PID {os.getpid()}] Caught {sig_name}! Starting graceful drain (1s)...\n")
    sys.stderr.flush()
    time.sleep(1)
    sys.stderr.write(f"[server.py PID {os.getpid()}] Clean shutdown complete. Exiting.\n")
    sys.stderr.flush()
    RUNNING = False
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

class ProcessInfoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        info = {
            "pid": os.getpid(),
            "ppid": os.getppid(),
            "cwd": os.getcwd(),
            "app_env": os.environ.get("APP_ENV", "unset"),
            "argv": sys.argv,
        }
        body = json.dumps(info, indent=2).encode("utf-8")
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        
    def log_message(self, format, *args):
        sys.stdout.write(f"[STDOUT PID {os.getpid()}] " + (format % args) + "\n")
        sys.stdout.flush()

def run():
    print(f"--- Process Starting ---")
    print(f"PID:      {os.getpid()}")
    print(f"PPID:     {os.getppid()}")
    print(f"APP_ENV:  {os.environ.get('APP_ENV', 'unset')}")
    print(f"Listening on http://{HOST}:{PORT}")
    sys.stdout.flush()
    
    server = http.server.HTTPServer((HOST, PORT), ProcessInfoHandler)
    server.timeout = 0.5
    while RUNNING:
        server.handle_request()

if __name__ == "__main__":
    run()
