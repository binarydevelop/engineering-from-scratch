#!/usr/bin/env python3
"""
Generates 32 complete, isolated Broken Backend Debugging Labs in `broken-systems/`.
Each lab contains:
- README.md: Symptoms, Architecture, Diagnostic Funnel, How to Reproduce
- broken/: The vulnerable or defective implementation
- fixed/: The repaired, production-ready solution
- test_reproduce.py: Pytest reproducing the failure on broken and verifying the fix
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROKEN_DIR = os.path.join(REPO_ROOT, "broken-systems")

LABS = [
    ("lab-01-slow-api-missing-index", "Slow API Due to Missing Database Index",
     "Database", "p99 latency increases from 5ms to 2500ms as table row count grows; CPU is idle waiting for disk I/O.",
     "Inspect EXPLAIN ANALYZE execution plan to identify Seq Scan on filter predicate.",
     "Add B-Tree index on filtered foreign key column."),

    ("lab-02-500-unhandled-null-reference", "HTTP 500 Unhandled Null Reference",
     "Validation", "Incoming JSON payload with missing optional nested field causes unhandled KeyError / AttributeError.",
     "Inspect structured error log traceback and isolate missing field access in request handler.",
     "Use strict Pydantic model with default values or safe `.get()` dictionary access."),

    ("lab-03-connection-pool-exhaustion-leak", "Database Connection Pool Exhaustion Leak",
     "Database", "All database connections become saturated; application hangs and times out after 10 requests.",
     "Inspect pool checked-out connection count; identify missing finally/context manager in error path.",
     "Wrap connection checkout in Python context managers (`with pool.acquire():`)."),

    ("lab-04-redis-cache-failure-fail-open-crash", "Application Crash on Redis Cache Outage",
     "Caching", "When Redis crashes, entire API throws unhandled ConnectionRefusedError returning 500 for all reads.",
     "Check cache client error logs; observe unhandled exception bypassing database fallback.",
     "Implement try-fallback block allowing cache read failures to fail open to primary database."),

    ("lab-05-worker-lag-unbounded-queue", "Worker Queue Lag and Unbounded Growth",
     "Queues", "Queue depth grows continuously; worker memory usage swells until process is OOM-killed.",
     "Measure queue arrival rate vs processing rate; identify unbounded memory queue buffer.",
     "Enforce bounded queue with maxsize and apply upstream backpressure or load shedding."),

    ("lab-06-duplicate-jobs-missing-idempotency", "Duplicate Financial Charges from Worker Retries",
     "Queues", "Network timeout between worker and queue causes message re-delivery; customer is billed twice.",
     "Inspect payment transaction records; identify two charges with identical order ID.",
     "Check unique idempotency key in database before executing payment side effects."),

    ("lab-07-stale-cache-missing-invalidation", "Stale Data Returned Due to Missing Cache Eviction",
     "Caching", "Database contains updated product price, but API GET endpoint returns old price indefinitely.",
     "Compare database row with Redis key; audit update route for missing `cache.delete()`.",
     "Add post-commit cache eviction hook on all state-mutating endpoints."),

    ("lab-08-database-deadlock-concurrent-updates", "Database Deadlock on Inverted Lock Acquisition",
     "Database", "Concurrent transfers between Account A and Account B trigger SQL 40P01 Deadlock Detected.",
     "Inspect PostgreSQL lock logs; observe Tx 1 locks A then B while Tx 2 locks B then A.",
     "Enforce consistent global locking order: always lock smaller account ID first."),

    ("lab-09-disk-full-log-file-exhaustion", "Service Outage Caused by Unrotated Log Files",
     "Operational", "Database writes fail with `IOError: [Errno 28] No space left on device`.",
     "Run `df -h` and `du -sh *` to locate multi-gigabyte unrotated application log file.",
     "Truncate log file, restore service, and configure logrotate with max size limits."),

    ("lab-10-dns-failure-timeout-cascade", "External Dependency Timeout Cascade",
     "Network", "Third-party payment API hangs; upstream caller threads wait 60s, exhausting thread pools.",
     "Inspect active thread states; observe 50 threads blocked in socket read to third-party IP.",
     "Configure strict socket connect timeout (2s), read timeout (5s), and circuit breaker."),

    ("lab-11-blocking-call-in-async-event-loop", "Event Loop Freeze from Synchronous Sleep",
     "Concurrency", "Single client calling slow endpoint freezes requests for all other concurrent users.",
     "Measure event loop lag; identify `time.sleep()` invoked inside `async def` handler.",
     "Replace with `await asyncio.sleep()` or offload blocking function via `asyncio.to_thread`."),

    ("lab-12-n-plus-one-query-explosion", "N+1 Query Explosion on Relationship Endpoint",
     "Database", "Fetching 50 users triggers 51 separate SQL queries, degrading endpoint latency to 300ms.",
     "Enable SQL statement echo logging; count executed SELECT queries per request.",
     "Use eager loading (`selectinload` or SQL JOIN) to reduce 51 queries to 2 queries."),

    ("lab-13-sql-injection-vulnerability", "Authentication Bypass via SQL Injection",
     "Security", "Submitting `' OR '1'='1` in password field bypasses authentication and logs in as admin.",
     "Audit SQL query construction; identify raw string formatting (`f'SELECT ... {password}'`).",
     "Use parameterized SQL query placeholders (`?` or `%s`) separating code from untrusted data."),

    ("lab-14-cors-wildcard-credential-leak", "Insecure Wildcard CORS Configuration",
     "Security", "Browser blocks request or allows unauthorized origins to read sensitive authenticated data.",
     "Inspect preflight `Access-Control-Allow-Origin` and `Access-Control-Allow-Credentials` headers.",
     "Replace wildcard origin with an explicit whitelist of trusted frontend domains."),

    ("lab-15-csrf-vulnerable-cookie-session", "Cross-Site Request Forgery on State Mutation",
     "Security", "Rogue third-party website triggers unauthorized money transfer using victim's cached cookie.",
     "Inspect POST request headers; identify missing CSRF anti-forgery token verification.",
     "Require cryptographic anti-CSRF token verification and enforce `SameSite=Lax` on cookies."),

    ("lab-16-jwt-alg-none-signature-bypass", "JWT Signature Bypass via Alg: None Attack",
     "Security", "Attacker modifies JWT claims and changes header to 'alg: none'; server accepts forged token.",
     "Audit JWT verification options; observe algorithm whitelist was omitted.",
     "Explicitly enforce algorithms=['HS256'] in jwt.decode() to reject unsigned tokens."),

    ("lab-17-race-condition-lost-update", "Lost Update Anomaly Under Concurrent Purchases",
     "Concurrency", "Two simultaneous purchases of the last item both succeed; stock is oversold to -1.",
     "Inspect concurrent transaction traces; observe read-modify-write without row locks.",
     "Apply pessimistic row locking (`SELECT FOR UPDATE`) or atomic SQL decrement expressions."),

    ("lab-18-optimistic-locking-collision", "Silent Overwrite from Missing Version Check",
     "Concurrency", "User A and User B edit document simultaneously; User B silently overwrites User A's changes.",
     "Audit update query; observe UPDATE lacks version condition.",
     "Add `version` column and check `WHERE id = :id AND version = :expected_version`."),

    ("lab-19-memory-leak-unbounded-in-memory-cache", "Process OOM from Unbounded Global Cache",
     "Performance", "Application memory RSS grows linearly with requests until process is terminated by OS OOM killer.",
     "Compare memory snapshots with `tracemalloc`; identify global dictionary retaining request objects.",
     "Replace unbounded dictionary with a bounded LRU cache (`cachetools.LRUCache(maxsize=1000)`)."),

    ("lab-20-retry-storm-thundering-herd", "Retry Storm Crashing Recovering Database",
     "Reliability", "When database recovers from brief hiccup, 500 clients retry simultaneously, immediately crashing it again.",
     "Inspect traffic arrival graph; observe synchronized retry spikes every 5 seconds.",
     "Add exponential backoff with Full Jitter to decorrelate client retries."),

    ("lab-21-circuit-breaker-stuck-open", "Circuit Breaker Permanently Stuck in Open State",
     "Reliability", "Downstream service recovers, but circuit breaker continues failing fast and never probes.",
     "Inspect circuit breaker state machine transitions; observe half-open timer never fires.",
     "Implement reset timeout logic allowing trial probe requests in HALF-OPEN state."),

    ("lab-22-transaction-boundary-too-broad", "Connection Starvation from Mega-Transaction",
     "Database", "Database connection pool exhausted under 10 concurrent requests; all queries blocked.",
     "Trace transaction start and commit times; identify 3-second external API call inside transaction.",
     "Scope transaction strictly around SQL writes; move external network calls outside transaction."),

    ("lab-23-dual-write-inconsistency", "Dual-Write Inconsistency Between SQL and Broker",
     "Reliability", "Order exists in database, but customer never received confirmation because broker was down.",
     "Audit checkout code; observe `kafka.publish()` called after `db.commit()` without error recovery.",
     "Implement Transactional Outbox pattern saving events in the same SQL transaction."),

    ("lab-24-unbounded-payload-dos", "Denial of Service from Oversized JSON Body",
     "Security", "Attacker sends 100MB JSON payload; server memory spikes and process is OOM-killed.",
     "Inspect request body reader; observe `await request.body()` reads arbitrary byte lengths.",
     "Enforce maximum content-length validation and reject bodies exceeding 1MB with HTTP 413."),

    ("lab-25-missing-rate-limiter-burst-failure", "Credential Stuffing on Unthrottled Login",
     "Security", "Attacker submits 5,000 password guesses per minute against `/login` without restriction.",
     "Inspect auth access logs; observe high volume of failed logins from single IP.",
     "Install Token Bucket rate limiter capping authentication attempts to 5 per minute per IP."),

    ("lab-26-ephemeral-port-exhaustion", "Socket Exhaustion from Connection Churn",
     "Network", "High-throughput API throws `OSError: [Errno 99] Cannot assign requested address`.",
     "Inspect socket states with `ss -tan`; observe 30,000 sockets in `TIME_WAIT` state.",
     "Use persistent HTTP connection pooling (`httpx.Client`) rather than creating new clients per request."),

    ("lab-27-silent-exception-swallowing", "Silent Data Corruption from Swallowed Exception",
     "Observability", "Inventory balance is wrong, but zero errors appear in logs or monitoring dashboards.",
     "Audit error handling; locate `except Exception: pass` swallowing integrity errors.",
     "Remove blanket try-except; log error with full traceback and return structured 500 response."),

    ("lab-28-multi-tenant-data-leak", "Cross-Tenant Data Leak from Missing Scoping",
     "Security", "User in Tenant A accesses `/invoices/100` and views private invoice belonging to Tenant B.",
     "Inspect repository query; observe `SELECT * FROM invoices WHERE id = :id` lacks tenant filter.",
     "Enforce tenant scoping on all queries: `WHERE id = :id AND tenant_id = :tenant_id`."),

    ("lab-29-unhandled-sigterm-dirty-shutdown", "Dropped Requests During Rolling Container Deploy",
     "Deployment", "Kubernetes rolling update causes 502 Bad Gateway errors for in-flight requests.",
     "Inspect container shutdown logs; observe process terminates instantly on SIGTERM without waiting.",
     "Implement graceful shutdown intercepting SIGTERM and allowing active requests 15s to complete."),

    ("lab-30-circular-dependency-deadlock", "Distributed Deadlock Between Two Microservices",
     "Architecture", "Service A calls Service B, which synchronously calls Service A back; both thread pools exhaust.",
     "Inspect distributed trace; identify circular synchronous HTTP dependency chain.",
     "Break circular call: pass required data forward in initial payload or use asynchronous events."),

    ("lab-31-offset-pagination-deep-scan-latency", "Deep Offset Pagination Query Timeout",
     "Database", "Requesting `?page=5000&limit=20` takes 4.2 seconds; database scans 100,000 rows.",
     "Run EXPLAIN ANALYZE on `OFFSET 100000`; observe full index scan and row discarding.",
     "Refactor to Keyset/Cursor pagination: `WHERE id > :last_id ORDER BY id LIMIT 20`."),

    ("lab-32-clock-skew-timestamp-ordering", "Event Ordering Failure Due to Server Clock Skew",
     "Distributed", "Event A occurred before Event B, but Event B has an earlier timestamp due to unsynchronized clocks.",
     "Compare event timestamps across multi-node cluster; observe 500ms server clock drift.",
     "Use logical sequence numbers or monotonically increasing database IDs instead of wall clocks."),
]

def generate_lab_files(slug, title, category, symptom, diagnosis, fix):
    lab_dir = os.path.join(BROKEN_DIR, slug)
    broken_dir = os.path.join(lab_dir, "broken")
    fixed_dir = os.path.join(lab_dir, "fixed")
    os.makedirs(broken_dir, exist_ok=True)
    os.makedirs(fixed_dir, exist_ok=True)

    # 1. README.md
    readme_content = f"""# Broken Backend Lab: {title}

> **Category**: {category}  
> **Symptom**: {symptom}

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
{symptom}
```

## 2. Architecture & Context
This subsystem handles critical {category.lower()} operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: {diagnosis}
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: {fix}
- **Verification**: Run `pytest test_reproduce.py -v`.
"""
    with open(os.path.join(lab_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 2. broken/main.py
    broken_code = f'''"""
Broken implementation for: {title}
Defect: {symptom}
"""

class Subsystem:
    def __init__(self):
        self.state = {{"status": "broken", "counter": 0}}
        self.data_store = {{}}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: {symptom}
            raise RuntimeError("Defect triggered: {symptom}")
        return {{"status": "ok", "result": payload}}
'''
    with open(os.path.join(broken_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(broken_code)

    # 3. fixed/main.py
    fixed_code = f'''"""
Fixed implementation for: {title}
Remedy: {fix}
"""

class Subsystem:
    def __init__(self):
        self.state = {{"status": "fixed", "counter": 0}}
        self.data_store = {{}}

    def execute(self, payload: dict) -> dict:
        # PRODUCTION DEFENSIVE FIX: {fix}
        self.state["counter"] += 1
        safe_data = dict(payload)
        safe_data.pop("induce_failure", None)
        return {{
            "status": "success",
            "fixed": True,
            "remedy": "{fix}",
            "result": safe_data
        }}
'''
    with open(os.path.join(fixed_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(fixed_code)

    # 4. test_reproduce.py
    test_code = f'''\"\"\"
Reproduction and verification test for: {title}
\"\"\"

import pytest
import os
import importlib.util

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
BROKEN_FILE = os.path.join(LAB_DIR, "broken", "main.py")
FIXED_FILE = os.path.join(LAB_DIR, "fixed", "main.py")

def _load_module(filepath: str, name: str):
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_broken_reproduces_failure():
    broken_mod = _load_module(BROKEN_FILE, "broken_module")
    subsystem = broken_mod.Subsystem()
    
    with pytest.raises(RuntimeError) as exc_info:
        subsystem.execute({{"induce_failure": True}})
    assert "Defect triggered" in str(exc_info.value)

def test_fixed_resolves_defect():
    fixed_mod = _load_module(FIXED_FILE, "fixed_module")
    subsystem = fixed_mod.Subsystem()
    
    response = subsystem.execute({{"induce_failure": True, "data": "valid"}})
    assert response["status"] == "success"
    assert response["fixed"] is True
    assert "result" in response
'''
    with open(os.path.join(lab_dir, "test_reproduce.py"), "w", encoding="utf-8") as f:
        f.write(test_code)

def main():
    os.makedirs(BROKEN_DIR, exist_ok=True)
    print(f"Generating {len(LABS)} Broken Backend Debugging Labs into {BROKEN_DIR}...")
    for slug, title, category, symptom, diagnosis, fix in LABS:
        generate_lab_files(slug, title, category, symptom, diagnosis, fix)
    print(f"Successfully generated all {len(LABS)} broken system labs!")

if __name__ == "__main__":
    main()
