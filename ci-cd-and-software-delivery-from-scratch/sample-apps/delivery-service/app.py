#!/usr/bin/env python3
"""
Delivery Service — Sample Production Backend Application
Designed for CI/CD and Software Delivery Engineering.

Implements Twelve-Factor App principles:
- Config stored in environment variables
- Strict health probe endpoints (/health/liveness, /health/readiness)
- Immutable build identity metadata (/version)
- Feature flag management (/api/flags)
- Database persistence with schema migration awareness
"""

import json
import os
import sqlite3
import sys
import time
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional

# --- Configuration (Twelve-Factor App) ---
PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "delivery.db"))
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
GIT_COMMIT = os.environ.get("GIT_COMMIT", "HEAD-unknown")
ARTIFACT_DIGEST = os.environ.get("ARTIFACT_DIGEST", "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
BUILD_TIMESTAMP = os.environ.get("BUILD_TIMESTAMP", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

# In-memory feature flags (can be overridden via POST /api/flags)
FEATURE_FLAGS: Dict[str, bool] = {
    "enable_v2_pricing": False,
    "fast_checkout": True,
    "extended_telemetry": True
}


def get_db_connection() -> sqlite3.Connection:
    """Creates a connection to SQLite database and ensures schema exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initializes basic orders table if not present."""
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_email TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL
            );
        """)
    conn.close()


class DeliveryServiceHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler providing REST API and operational endpoints."""

    def _send_json(self, status_code: int, data: Dict[str, Any]):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("X-App-Version", APP_VERSION)
        self.send_header("X-Commit-SHA", GIT_COMMIT)
        self.end_headers()
        self.wfile.write(response_bytes)

    def log_message(self, format: str, *args):
        # Structured log format: [timestamp] [client_ip] "method path" code
        sys.stderr.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}\n")

    def do_GET(self):
        """Route GET requests."""
        if self.path == "/health/liveness":
            # Liveness: Is the process responsive?
            self._send_json(HTTPStatus.OK, {
                "status": "alive",
                "timestamp": time.time()
            })

        elif self.path == "/health/readiness":
            # Readiness: Can this replica serve traffic? (Verify DB connectivity)
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT 1")
                cur.fetchone()
                conn.close()
                self._send_json(HTTPStatus.OK, {
                    "status": "ready",
                    "database": "connected",
                    "environment": ENVIRONMENT
                })
            except Exception as e:
                self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {
                    "status": "not_ready",
                    "database_error": str(e),
                    "environment": ENVIRONMENT
                })

        elif self.path == "/health":
            # Unified health endpoint
            self.path = "/health/readiness"
            self.do_GET()

        elif self.path == "/version":
            # Production provenance and immutable build identity
            self._send_json(HTTPStatus.OK, {
                "service": "delivery-service",
                "version": APP_VERSION,
                "commit_sha": GIT_COMMIT,
                "artifact_digest": ARTIFACT_DIGEST,
                "build_timestamp": BUILD_TIMESTAMP,
                "environment": ENVIRONMENT
            })

        elif self.path == "/api/flags":
            # Feature flags inspection
            self._send_json(HTTPStatus.OK, {
                "flags": FEATURE_FLAGS
            })

        elif self.path == "/api/orders":
            # List orders
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, customer_email, amount_cents, status, created_at FROM orders ORDER BY id DESC LIMIT 50")
            rows = [dict(row) for row in cur.fetchall()]
            conn.close()
            self._send_json(HTTPStatus.OK, {
                "count": len(rows),
                "orders": rows
            })

        else:
            self._send_json(HTTPStatus.NOT_FOUND, {
                "error": "Not Found",
                "path": self.path
            })

    def do_POST(self):
        """Route POST requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            body = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON payload"})
            return

        if self.path == "/api/orders":
            customer_email = body.get("customer_email")
            amount_cents = body.get("amount_cents")
            if not customer_email or amount_cents is None or not isinstance(amount_cents, int):
                self._send_json(HTTPStatus.BAD_REQUEST, {
                    "error": "Validation failed: 'customer_email' (str) and 'amount_cents' (int) are required"
                })
                return

            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            conn = get_db_connection()
            with conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO orders (customer_email, amount_cents, status, created_at) VALUES (?, ?, 'pending', ?)",
                    (customer_email, amount_cents, now)
                )
                order_id = cur.lastrowid
            conn.close()

            self._send_json(HTTPStatus.CREATED, {
                "message": "Order created successfully",
                "order": {
                    "id": order_id,
                    "customer_email": customer_email,
                    "amount_cents": amount_cents,
                    "status": "pending",
                    "created_at": now
                }
            })

        elif self.path == "/api/flags":
            key = body.get("key")
            value = body.get("value")
            if key in FEATURE_FLAGS and isinstance(value, bool):
                FEATURE_FLAGS[key] = value
                self._send_json(HTTPStatus.OK, {
                    "message": f"Flag '{key}' updated to {value}",
                    "flags": FEATURE_FLAGS
                })
            else:
                self._send_json(HTTPStatus.BAD_REQUEST, {
                    "error": f"Unknown flag key '{key}' or value is not boolean"
                })

        else:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not Found", "path": self.path})


def run_server():
    init_database()
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, DeliveryServiceHandler)
    sys.stderr.write(f"Delivery Service v{APP_VERSION} ({GIT_COMMIT[:7]}) listening on {HOST}:{PORT}\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.stderr.write("Server stopped.\n")


if __name__ == "__main__":
    run_server()
