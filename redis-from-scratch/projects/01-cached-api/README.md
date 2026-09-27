# Project 01: Production-Grade Cached REST API

Demonstrates the Cache-Aside pattern, stale read prevention, metrics instrumentation, and single-flight mutex locking to solve the Cache Stampede (Thundering Herd) problem.

---

## Architecture

```text
HTTP Client
    │
    ▼
Fast API Server (Port 8080)
    │
    ├── 1. Query Redis Cache (cache:product:prod_1)
    │       ├── HIT ──► Return cached JSON (<1ms)
    │       └── MISS ─┐
    │                 ▼
    │          2. Mutex Lock (lock:product:prod_1 NX EX 3)
    │                 ├── Acquired ──► Query Database (20ms) ──► Populate Cache
    │                 └── Contended ─► Backoff & Retry Cache Read
    │
    └── 3. POST /product/prod_1 ──► Updates DB & Issues DEL cache:product:prod_1
```

---

## How to Run

1. Start Redis:
   ```bash
   make up   # Or: ./scripts/start-redis.sh
   ```

2. Start the API server:
   ```bash
   python3 projects/01-cached-api/server.py
   ```

3. Run the concurrent load tester:
   ```bash
   python3 projects/01-cached-api/test_client.py
   ```

4. Check live metrics:
   ```bash
   curl http://localhost:8080/metrics
   ```
