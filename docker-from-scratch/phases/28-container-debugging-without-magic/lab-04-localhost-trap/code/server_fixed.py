#!/usr/bin/env python3
import http.server

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Connected to server bound to 0.0.0.0 (All interfaces)!\n")

if __name__ == "__main__":
    # FIXED: Binding to INADDR_ANY (0.0.0.0) listens on all interfaces (lo and eth0)
    print("[SERVER] Binding to 0.0.0.0:8080 (All interfaces)...")
    server = http.server.HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()
