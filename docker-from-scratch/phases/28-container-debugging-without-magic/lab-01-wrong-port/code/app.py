#!/usr/bin/env python3
import http.server

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Port Mismatch Resolved Successfully!\n")

if __name__ == "__main__":
    print("[APP] Starting web server listening internally on 0.0.0.0:8000...")
    server = http.server.HTTPServer(("0.0.0.0", 8000), Handler)
    server.serve_forever()
