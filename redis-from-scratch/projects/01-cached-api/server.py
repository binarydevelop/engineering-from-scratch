#!/usr/bin/env python3
"""
projects/01-cached-api/server.py — Resilient Cache-Aside HTTP Service

Features:
1. Cache-Aside pattern (Redis -> SQLite database fallback)
2. Cache hit/miss instrumentation and latency tracking
3. Explicit cache invalidation on updates
4. Single-Flight Mutex locking to prevent Cache Stampedes under high concurrency
"""

import http.server
import json
import sqlite3
import socket
import time
import os
import threading
from urllib.parse import urlparse, parse_qs

DB_FILE = "/tmp/cached_api_db.sqlite"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Metrics counters
METRICS = {
    "total_requests": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "db_queries": 0,
    "stampede_locks_acquired": 0
}
METRICS_LOCK = threading.Lock()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, name TEXT, price REAL, stock INT);")
    # Seed 10 sample products
    for i in range(1, 11):
        cur.execute("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?);",
                    (f"prod_{i}", f"High Performance Widget {i}", 19.99 * i, 100))
    conn.commit()
    conn.close()

def redis_cmd(*args):
    """Minimal zero-dependency RESP socket client."""
    s = socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=1.0)
    # Format RESP array
    msg = f"*{len(args)}\r\n"
    for arg in args:
        s_arg = str(arg)
        msg += f"${len(s_arg.encode('utf-8'))}\r\n{s_arg}\r\n"
    s.sendall(msg.encode("utf-8"))
    
    # Read response
    resp = s.recv(4096).decode("utf-8", errors="replace")
    s.close()
    return resp

def redis_get(key):
    try:
        raw = redis_cmd("GET", key)
        if raw.startswith("$-1"):
            return None
        if raw.startswith("$"):
            # Format: $len\r\nvalue\r\n
            parts = raw.split("\r\n", 2)
            return parts[1]
        return None
    except Exception:
        return None

def redis_set_ex(key, value, ttl_sec):
    try:
        redis_cmd("SET", key, value, "EX", ttl_sec)
    except Exception:
        pass

def redis_del(key):
    try:
        redis_cmd("DEL", key)
    except Exception:
        pass

def acquire_stampede_lock(key, ttl_sec=5):
    """Atomic distributed lock: SET lock:<key> <token> NX EX <ttl>"""
    try:
        resp = redis_cmd("SET", f"lock:{key}", "locked", "NX", "EX", ttl_sec)
        return "+OK" in resp
    except Exception:
        return True # Fallback to direct DB query if Redis fails

def release_stampede_lock(key):
    try:
        redis_cmd("DEL", f"lock:{key}")
    except Exception:
        pass

class CachedApiHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Suppress default noisy console logs

    def do_GET(self):
        t0 = time.perf_counter()
        parsed = urlparse(self.path)
        
        if parsed.path == "/metrics":
            with METRICS_LOCK:
                hit_rate = (METRICS["cache_hits"] / max(1, METRICS["total_requests"])) * 100
                data = {**METRICS, "hit_rate_pct": round(hit_rate, 2)}
            self.send_json(200, data)
            return

        if parsed.path.startswith("/product/"):
            prod_id = parsed.path.split("/")[-1]
            cache_key = f"cache:product:{prod_id}"
            
            with METRICS_LOCK:
                METRICS["total_requests"] += 1

            # 1. Check Redis Cache
            cached = redis_get(cache_key)
            if cached:
                with METRICS_LOCK:
                    METRICS["cache_hits"] += 1
                elapsed_ms = (time.perf_counter() - t0) * 1000
                data = json.loads(cached)
                data["_source"] = "redis_cache"
                data["_latency_ms"] = round(elapsed_ms, 3)
                self.send_json(200, data)
                return

            # Cache Miss
            with METRICS_LOCK:
                METRICS["cache_misses"] += 1

            # 2. Stampede Protection via Mutex Lock
            locked = acquire_stampede_lock(prod_id, ttl_sec=3)
            if not locked:
                # Another worker is refreshing the cache; sleep and retry cache read
                for _ in range(10):
                    time.sleep(0.05)
                    cached = redis_get(cache_key)
                    if cached:
                        data = json.loads(cached)
                        data["_source"] = "redis_cache_after_stampede_wait"
                        data["_latency_ms"] = round((time.perf_counter() - t0) * 1000, 3)
                        self.send_json(200, data)
                        return

            with METRICS_LOCK:
                METRICS["stampede_locks_acquired"] += 1
                METRICS["db_queries"] += 1

            # 3. Query Persistent Database (simulated 20ms disk latency)
            time.sleep(0.02)
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("SELECT id, name, price, stock FROM products WHERE id = ?", (prod_id,))
            row = cur.fetchone()
            conn.close()

            if not row:
                release_stampede_lock(prod_id)
                self.send_json(404, {"error": "Product not found"})
                return

            prod_data = {"id": row[0], "name": row[1], "price": row[2], "stock": row[3]}
            
            # 4. Populate Cache with TTL (15 seconds)
            redis_set_ex(cache_key, json.dumps(prod_data), ttl_sec=15)
            release_stampede_lock(prod_id)

            elapsed_ms = (time.perf_counter() - t0) * 1000
            prod_data["_source"] = "sqlite_database"
            prod_data["_latency_ms"] = round(elapsed_ms, 3)
            self.send_json(200, prod_data)
            return

        self.send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        # Update product -> invalidate cache!
        parsed = urlparse(self.path)
        if parsed.path.startswith("/product/"):
            prod_id = parsed.path.split("/")[-1]
            length = int(self.headers.get("content-length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}
            
            new_price = body.get("price", 99.99)
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, prod_id))
            conn.commit()
            conn.close()

            # Cache Invalidation (Delete from Redis)
            redis_del(f"cache:product:{prod_id}")
            self.send_json(200, {"status": "updated", "invalidated_cache_key": f"cache:product:{prod_id}"})
            return

        self.send_json(404, {"error": "Not found"})

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def run():
    init_db()
    server = http.server.ThreadingHTTPServer(("0.0.0.0", 8080), CachedApiHandler)
    print("Cached API listening on http://0.0.0.0:8080 (Press Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == "__main__":
    run()
