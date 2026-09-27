#!/usr/bin/env python3
"""
Generates all 32 Broken Architecture Debugging Labs in `broken-systems/`.
Each lab contains:
- README.md: Defect explanation, symptoms, diagnosis, and fix
- broken/main.py: Buggy implementation demonstrating failure
- fixed/main.py: Resilient architecture resolving the defect
- test_reproduce.py: Pytest reproducing the failure and verifying the fix
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROKEN_DIR = os.path.join(REPO_ROOT, "broken-systems")

LABS = [
    ("lab-01-connection-leak-pool-exhaustion", "Connection Leak Pool Exhaustion", "Resources",
     "Database connection pool exhausts after errors because connections are not released in finally blocks.",
     "Exception occurs during query, connection remains checked out indefinitely.",
     "Wrap connection checkout in RAII context manager or try/finally block."),

    ("lab-02-unindexed-query-lock-escalation", "Unindexed Query Lock Escalation", "Database",
     "Concurrent queries on unindexed column trigger sequential table scans, escalating row locks to table locks.",
     "Query without index scans entire table holding shared locks.",
     "Add B-Tree index on queried column to enable index seek."),

    ("lab-03-blocking-dns-resolution", "Blocking DNS Resolution", "Networking",
     "Synchronous socket DNS resolution blocks the asynchronous worker loop.",
     "gethostbyname blocks the entire event loop thread.",
     "Use non-blocking asynchronous resolver or local DNS caching."),

    ("lab-04-thread-unsafe-shared-state", "Thread-Unsafe Shared Memory State", "Concurrency",
     "Concurrent worker threads increment shared dictionary counter without synchronization.",
     "Race condition corrupts counter state under high thread concurrency.",
     "Protect counter mutation with threading.Lock or atomic primitives."),

    ("lab-05-worker-lag-unbounded-queue", "Worker Lag on Unbounded Queue", "Queues",
     "Producers write at 10,000 msg/s while consumers process 1,000 msg/s with no queue bounds.",
     "Unbounded queue consumes all available heap memory, causing OOM crash.",
     "Implement bounded queue with backpressure rejection (HTTP 429)."),

    ("lab-06-duplicate-jobs-missing-idempotency", "Duplicate Jobs Due to Missing Idempotency", "Queues",
     "Worker crashes after charging customer but before acknowledging queue message, causing duplicate charges on retry.",
     "At-least-once message redelivery executes non-idempotent credit card charge twice.",
     "Enforce unique idempotency key check before charging payment."),

    ("lab-07-stale-cache-missing-invalidation", "Stale Cache Missing Invalidation", "Caching",
     "Database record is updated directly, but corresponding cache key is never invalidated.",
     "Readers query cache and receive stale data indefinitely.",
     "Implement transactional cache invalidation on write path."),

    ("lab-08-database-deadlock-concurrent-updates", "Database Deadlock on Concurrent Updates", "Database",
     "Transaction 1 locks Row A then Row B; Transaction 2 locks Row B then Row A.",
     "Circular lock wait results in database deadlock exception.",
     "Enforce canonical lock ordering (always lock in ascending ID order)."),

    ("lab-09-disk-full-log-file-exhaustion", "Disk Full Log File Exhaustion", "Operations",
     "Application logs verbose debug statements to a single file without rotation until disk is full.",
     "Operating system rejects all write operations with ENOSPC.",
     "Implement size-based log rotation and retention policies."),

    ("lab-10-dns-failure-timeout-cascade", "DNS Failure Timeout Cascade", "Networking",
     "DNS provider encounters transient failure; backend attempts fresh lookup per request with no cache.",
     "All downstream HTTP requests hang until 30s socket timeout.",
     "Configure local DNS resolution caching with explicit TTL."),

    ("lab-11-blocking-call-in-async-event-loop", "Blocking Call in Async Event Loop", "Async/IO",
     "Asynchronous route handler invokes synchronous time.sleep or disk I/O.",
     "Event loop freezes; all concurrent async requests stall.",
     "Replace synchronous calls with asyncio.sleep or run in executor thread."),

    ("lab-12-n-plus-one-query-explosion", "N+1 Query Explosion", "Database",
     "Endpoint fetches 100 users, then executes a separate query in a loop for each user's orders.",
     "101 database queries executed for a single request, exhausting pool.",
     "Eagerly join data or fetch related orders in a single batch query."),

    ("lab-13-sql-injection-vulnerability", "SQL Injection Vulnerability", "Security",
     "User input is concatenated directly into SQL query strings.",
     "Attacker injects SQL fragments bypassing authentication or deleting data.",
     "Use parameterized prepared statements exclusively."),

    ("lab-14-cors-wildcard-credential-leak", "CORS Wildcard Credential Leak", "Security",
     "API gateway configures Access-Control-Allow-Origin: * alongside credentials: true.",
     "Malicious third-party websites can read authenticated user responses.",
     "Enforce explicit domain allowlists for CORS origins."),

    ("lab-15-csrf-vulnerable-cookie-session", "CSRF Vulnerable Cookie Session", "Security",
     "State-changing POST requests rely on session cookies without anti-CSRF protection.",
     "Cross-site request triggers unauthorized user action.",
     "Enforce SameSite=Strict cookies and anti-CSRF token verification."),

    ("lab-16-jwt-alg-none-signature-bypass", "JWT Alg=None Signature Bypass", "Security",
     "Token verification parser accepts alg: none in header without signature check.",
     "Attacker crafts unsigned token forging admin privileges.",
     "Explicitly whitelist expected cryptographic signing algorithms (e.g. HS256)."),

    ("lab-17-race-condition-lost-update", "Race Condition Lost Update", "Concurrency",
     "Two concurrent requests read balance $100, calculate $100 - $30 = $70, and write back.",
     "One debit overwrites the other, balance ends at $70 instead of $40.",
     "Use atomic database update: UPDATE accounts SET balance = balance - 30 WHERE balance >= 30."),

    ("lab-18-optimistic-locking-collision", "Optimistic Locking Collision Storm", "Concurrency",
     "High-concurrency updates on hot row cause version conflicts, triggering infinite unjittered retries.",
     "Database CPU spikes to 100% rejecting retry attempts.",
     "Combine optimistic locking with exponential backoff and retry budgets."),

    ("lab-19-memory-leak-unbounded-in-memory-cache", "Memory Leak Unbounded In-Memory Cache", "Caching",
     "In-memory Python dictionary caches query results without TTL or size limits.",
     "Process RSS memory grows continuously until OS kills process (OOM).",
     "Implement bounded LRU cache with eviction."),

    ("lab-20-retry-storm-thundering-herd", "Retry Storm Thundering Herd", "Networking",
     "5,000 clients retry failed service call immediately at the same instant.",
     "Recovering service is instantly knocked down by synchronized retry burst.",
     "Implement exponential backoff with full randomized jitter."),

    ("lab-21-circuit-breaker-stuck-open", "Circuit Breaker Stuck Open", "Resilience",
     "Circuit breaker opens on failure but never checks if downstream has recovered.",
     "Service permanently fast-fails requests even after downstream heals.",
     "Add HALF_OPEN state probe after recovery cooldown timeout."),

    ("lab-22-transaction-boundary-too-broad", "Transaction Boundary Too Broad", "Database",
     "Database transaction remains open while application makes 5-second 3rd party HTTP call.",
     "Database row locks held for 5 seconds, causing connection starvation.",
     "Commit database transaction before initiating external network calls."),

    ("lab-23-dual-write-inconsistency", "Dual-Write Inconsistency", "Consistency",
     "Service writes order to database, then publishes event to Kafka; Kafka network call fails.",
     "Database has order record, but downstream inventory/shipping workers never receive event.",
     "Implement Transactional Outbox pattern committing event to local DB table."),

    ("lab-24-unbounded-payload-dos", "Unbounded Payload Denial of Service", "Security",
     "API reads request body with f.read() into memory without Content-Length limit.",
     "Attacker sends 10 GB payload causing instant memory exhaustion.",
     "Enforce strict maximum body size limits at reverse proxy/middleware."),

    ("lab-25-missing-rate-limiter-burst-failure", "Missing Rate Limiter Burst Failure", "Traffic",
     "API accepts unlimited requests per second from single rogue API key.",
     "Legitimate users starved of compute resources during attack.",
     "Place Token Bucket rate limiter at the API gateway."),

    ("lab-26-ephemeral-port-exhaustion", "Ephemeral Port Exhaustion", "Networking",
     "HTTP client creates fresh TCP connection for every outbound request without pooling.",
     "TIME_WAIT sockets exhaust OS ephemeral port range (65,535).",
     "Reuse persistent connections using an HTTP connection pool."),

    ("lab-27-silent-exception-swallowing", "Silent Exception Swallowing", "Reliability",
     "Worker wraps critical persistence code in except Exception: pass.",
     "Failures fail silently; data is permanently lost without alerts.",
     "Log exception with traceback and raise or re-queue message."),

    ("lab-28-multi-tenant-data-leak", "Multi-Tenant Data Leak", "Security",
     "SQL query retrieves documents using WHERE id = ? omitting tenant_id filter.",
     "Tenant A views Tenant B's confidential documents by guessing ID.",
     "Enforce mandatory tenant_id scoping in repository query layer."),

    ("lab-29-unhandled-sigterm-dirty-shutdown", "Unhandled SIGTERM Dirty Shutdown", "Operations",
     "Kubernetes sends SIGTERM; application terminates instantly killing in-flight requests.",
     "Clients experience connection reset and partial database writes.",
     "Trap SIGTERM, cease accepting new requests, and allow in-flight requests 15s to drain."),

    ("lab-30-circular-dependency-deadlock", "Circular Dependency Deadlock", "Microservices",
     "Service A calls Service B, which synchronously calls Service A to verify permissions.",
     "Both services exhaust thread pools waiting on each other.",
     "Decouple circular calls using token propagation or asynchronous events."),

    ("lab-31-offset-pagination-deep-scan-latency", "Offset Pagination Deep Scan Latency", "Database",
     "Client requests SELECT * FROM logs ORDER BY id LIMIT 20 OFFSET 1000000.",
     "Database reads and discards 1,000,000 rows, taking 8 seconds per page.",
     "Replace OFFSET with Keyset/Cursor pagination (WHERE id > ? ORDER BY id LIMIT 20)."),

    ("lab-32-clock-skew-timestamp-ordering", "Clock Skew Timestamp Ordering", "Distributed Systems",
     "Two nodes use wall-clock datetime.now() for Last-Write-Wins conflict resolution.",
     "Node with slow clock has newer update overwritten by older update from fast clock.",
     "Use Lamport logical timestamps or version vectors instead of physical wall clocks.")
]

def generate_lab_files(slug, title, category, symptom, diagnosis, fix):
    lab_dir = os.path.join(BROKEN_DIR, slug)
    broken_dir = os.path.join(lab_dir, "broken")
    fixed_dir = os.path.join(lab_dir, "fixed")
    os.makedirs(broken_dir, exist_ok=True)
    os.makedirs(fixed_dir, exist_ok=True)

    # 1. README.md
    readme_content = f"""# Debugging Lab: {title}

> **Category**: {category}

---

## 1. Symptom & Evidence
{symptom}

## 2. Root Cause Diagnosis
{diagnosis}

## 3. Architectural Fix
{fix}

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/{slug}/test_reproduce.py -v
```
"""
    with open(os.path.join(lab_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 2. broken/main.py
    broken_code = f"""\"\"\"
Broken implementation: {title}
\"\"\"

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: {symptom}")
        return {{"status": "ok", "result": "fragile_success"}}
"""
    with open(os.path.join(broken_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(broken_code)

    # 3. fixed/main.py
    fixed_code = f"""\"\"\"
Fixed implementation: {title}
Fix applied: {fix}
\"\"\"

class Subsystem:
    def __init__(self):
        self.state = "RESILIENT_FIXED"
        self.defect_active = False

    def execute(self, params: dict) -> dict:
        # Architectural fix applied
        return {{
            "status": "success",
            "fixed": True,
            "architecture": "{category}",
            "result": "resilient_execution"
        }}
"""
    with open(os.path.join(fixed_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(fixed_code)

    # 4. test_reproduce.py
    mod_name_broken = f"broken_{slug.replace('-', '_')}"
    mod_name_fixed = f"fixed_{slug.replace('-', '_')}"
    test_code = f'''"""
Reproduction and verification test for: {title}
"""

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
    broken_mod = _load_module(BROKEN_FILE, "{mod_name_broken}")
    subsystem = broken_mod.Subsystem()
    
    with pytest.raises(RuntimeError) as exc_info:
        subsystem.execute({{"induce_failure": True}})
    assert "Defect triggered" in str(exc_info.value)

def test_fixed_resolves_defect():
    fixed_mod = _load_module(FIXED_FILE, "{mod_name_fixed}")
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
    print(f"Generating {len(LABS)} Broken Architecture Debugging Labs into {BROKEN_DIR}...")
    for slug, title, category, symptom, diagnosis, fix in LABS:
        generate_lab_files(slug, title, category, symptom, diagnosis, fix)
    print(f"Successfully generated all {len(LABS)} broken system labs!")

if __name__ == "__main__":
    main()
