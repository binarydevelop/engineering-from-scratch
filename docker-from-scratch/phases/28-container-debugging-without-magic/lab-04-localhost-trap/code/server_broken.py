#!/usr/bin/env python3
import http.server

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Connected to server bound to 127.0.0.1\n")

if __name__ == "__main__":
    # BUG: Binding to loopback interface 127.0.0.1 only!
    # Packets forwarded from host over eth0 will be dropped by the kernel!
    print("[SERVER] Binding to 127.0.0.1:8080 (Loopback only)...")
    server = http.server.HTTPServer(("127.0.0.1", 8080), Handler)
    server.serve_forever()
