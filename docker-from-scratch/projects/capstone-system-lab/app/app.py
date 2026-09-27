import os
import sys
import socket
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "0.0.0.0"
PORT = int(os.environ.get("APP_PORT", 8000))
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
NATS_HOST = os.environ.get("NATS_HOST", "nats")
NATS_PORT = int(os.environ.get("NATS_PORT", 4222))

REQUEST_COUNT = 0

def check_postgres(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((host, port))
        # Send PostgreSQL SSLRequest packet (8 bytes: length=8, code=80877103)
        s.sendall(b'\x00\x00\x00\x08\x04\xd2\x16/')
        resp = s.recv(1)
        s.close()
        if resp in (b'S', b'N'):
            return True, "postgres ready"
        return True, "tcp connected"
    except Exception as e:
        return False, str(e)

def check_redis(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((host, port))
        s.sendall(b"PING\r\n")
        resp = s.recv(1024)
        s.close()
        if b"+PONG" in resp:
            return True, "pong"
        return False, f"unexpected response: {resp}"
    except Exception as e:
        return False, str(e)

def check_nats(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((host, port))
        resp = s.recv(1024)
        s.close()
        if b"INFO" in resp:
            return True, "nats ready"
        return False, f"unexpected response: {resp}"
    except Exception as e:
        return False, str(e)

class SystemLabHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUEST_COUNT
        REQUEST_COUNT += 1

        if self.path == "/" or self.path == "":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {
                "message": "Welcome to the Capstone System Design Lab!",
                "version": "1.0.0",
                "hostname": socket.gethostname(),
                "endpoints": ["/health", "/metrics", "/services"]
            }
            self.wfile.write(json.dumps(payload, indent=2).encode())

        elif self.path == "/health":
            pg_ok, pg_msg = check_postgres(POSTGRES_HOST, POSTGRES_PORT)
            rd_ok, rd_msg = check_redis(REDIS_HOST, REDIS_PORT)
            nt_ok, nt_msg = check_nats(NATS_HOST, NATS_PORT)

            overall_healthy = pg_ok and rd_ok and nt_ok
            status_code = 200 if overall_healthy else 503

            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            payload = {
                "status": "healthy" if overall_healthy else "unhealthy",
                "timestamp": time.time(),
                "services": {
                    "postgres": {"status": "ok" if pg_ok else "down", "detail": pg_msg},
                    "redis": {"status": "ok" if rd_ok else "down", "detail": rd_msg},
                    "nats": {"status": "ok" if nt_ok else "down", "detail": nt_msg},
                }
            }
            self.wfile.write(json.dumps(payload, indent=2).encode())

        elif self.path == "/metrics":
            pg_ok, _ = check_postgres(POSTGRES_HOST, POSTGRES_PORT)
            rd_ok, _ = check_redis(REDIS_HOST, REDIS_PORT)
            nt_ok, _ = check_nats(NATS_HOST, NATS_PORT)

            metrics = [
                "# HELP system_lab_requests_total Total number of HTTP requests processed.",
                "# TYPE system_lab_requests_total counter",
                f"system_lab_requests_total {REQUEST_COUNT}",
                "",
                "# HELP system_lab_service_up Dependency service availability (1 = up, 0 = down).",
                "# TYPE system_lab_service_up gauge",
                f'system_lab_service_up{{service="postgres"}} {1 if pg_ok else 0}',
                f'system_lab_service_up{{service="redis"}} {1 if rd_ok else 0}',
                f'system_lab_service_up{{service="nats"}} {1 if nt_ok else 0}',
                ""
            ]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.end_headers()
            self.wfile.write("\n".join(metrics).encode())

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def log_message(self, format, *args):
        # Structured log format
        sys.stdout.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    print(f"[*] Starting System Lab App on port {PORT}...", flush=True)
    print(f"[*] Configured backends -> Postgres: {POSTGRES_HOST}:{POSTGRES_PORT}, Redis: {REDIS_HOST}:{REDIS_PORT}, NATS: {NATS_HOST}:{NATS_PORT}", flush=True)
    server = HTTPServer((HOST, PORT), SystemLabHandler)
    server.serve_forever()
