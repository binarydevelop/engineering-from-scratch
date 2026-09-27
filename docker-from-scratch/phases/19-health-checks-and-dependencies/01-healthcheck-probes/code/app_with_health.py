#!/usr/bin/env python3
"""
app_with_health.py
HTTP server that demonstrates process lifecycle vs application readiness.
Provides /healthz and /break endpoints.
"""

import http.server
import json
import time

PORT = 8080
START_TIME = time.time()
HEALTHY = True
WARMUP_SECONDS = 2

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global HEALTHY
        
        if self.path == "/healthz":
            # If warming up or manually broken, return failure
            uptime = time.time() - START_TIME
            if uptime < WARMUP_SECONDS:
                self.send_response(503)
                self.end_headers()
                self.wfile.write(b'{"status": "warming_up"}\n')
            elif not HEALTHY:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"status": "unhealthy_internal_error"}\n')
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status": "healthy"}\n')
                
        elif self.path == "/break":
            HEALTHY = False
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"action": "fault_injected", "HEALTHY": false}\n')
            
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"service": "active"}\n')

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()
