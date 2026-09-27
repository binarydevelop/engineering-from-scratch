# Systematic Backend Debugging Framework

> **Never Guess, Never Randomly Restart**: Randomly restarting services destroys critical volatile debugging evidence (memory state, active locks, thread backtraces, socket buffers). Always gather empirical evidence through structured diagnosis.

---

## The Systematic Diagnosis Funnel

When an outage, latency spike, or elevated error rate occurs, execute this sequence without skipping steps:

```text
                  [ 1. Symptom Definition ]
       What is failing? (HTTP 500, 504 Timeout, p99 Latency, Data Corruption)
                             │
                             ▼
               [ 2. Scope & Cardinality Check ]
       Which endpoint? Which user? Which tenant? Which geographic region?
                             │
                             ▼
             [ 3. Network Ingress & Traffic Flow ]
       Is traffic reaching the load balancer? Are sockets establishing?
                             │
                             ▼
               [ 4. Error vs Latency Isolation ]
         Is it failing fast (immediate 500) or failing slow (timeout)?
                             │
                             ▼
               [ 5. Application Log Correlation ]
       Trace correlation ID / request ID across structured logs and tracebacks.
                             │
                             ▼
               [ 6. Host & Process Resource Health ]
       CPU utilization, Memory RSS / OOM kills, File descriptor exhaustion.
                             │
                             ▼
             [ 7. Persistence & Database Saturation ]
       Active connections vs pool limit? Long-running queries? Row locks / Deadlocks?
                             │
                             ▼
               [ 8. Cache & Broker Health ]
       Redis latency? Cache hit ratio dropped? Queue depth backing up? Worker crashes?
                             │
                             ▼
             [ 9. Downstream External Dependencies ]
       Third-party payment/email APIs timing out or returning 429/500?
                             │
                             ▼
            [ 10. Temporal & Configuration Diff ]
       What changed? Recent git commit deploy? Environment variable update? Schema migration?
```

---

## Common Symptom to Root Cause Matrix

| Symptom | Initial Evidence | Primary Culprit | Verification Command / Step |
| :--- | :--- | :--- | :--- |
| **p99 Latency Doubled, CPU Low** | High response duration, negligible CPU load on app nodes. | Database connection pool exhaustion or unindexed query lock contention. | Inspect active SQL queries: `SELECT * FROM pg_stat_activity WHERE state != 'idle';` |
| **HTTP 502 Bad Gateway** | Nginx/ALB returns 502 immediately or after proxy timeout. | Upstream backend application process crashed, OOM killed, or socket backlog full. | `dmesg \| grep -i oom` or check systemd/container exit code. |
| **HTTP 504 Gateway Timeout** | Request hangs for 30s or 60s before returning 504. | Unbounded downstream call to external API or database query lacking a statement timeout. | Check application logs for the last span before the 60s mark; inspect socket states with `ss -tan`. |
| **Database Pool Timeout** | Log: `Timeout waiting for connection from pool`. | Connection leak (handler acquires connection but fails to release in `finally` block) or long-running transaction holding connection. | Trace active pool checked-out connections; review exception handling paths. |
| **Worker Queue Depth Exploding** | Redis/Queue length increases monotonically; latency on background tasks soars. | Worker processes crashed on a "poison pill" task lacking a DLQ, or task processing time exceeds arrival rate ($\lambda > \mu$). | Inspect worker logs for repeated identical exceptions; check worker process CPU/memory. |
| **Stale Data Returned** | Database contains updated value, but GET endpoint returns old value. | Cache invalidation failed, TTL set to infinity, or cache key naming collision across tenants. | Inspect Redis key: `redis-cli GET key_name`; check if write endpoint triggered invalidation. |
| **Spike in HTTP 409 Conflict** | High rate of concurrent update failures. | Optimistic locking version mismatch or unique constraint collision under concurrent traffic. | Inspect application retry logic and concurrent traffic arrival patterns. |
