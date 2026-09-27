# Production Troubleshooting & Latency Diagnosis Guide

> **Motto:** Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it.

When an application alerts on high latency or connection timeouts to Redis, never guess or blindly restart the server. Follow this systematic diagnostic tree.

---

## 1. The Root Cause Diagnostic Tree

```text
                        APPLICATION EXPERIENCING LATENCY SPIKE
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         [ Is Host CPU 100%? ]                         [ Is Host CPU Normal (<30%)? ]
                  │                                               │
        ┌─────────┴─────────┐                           ┌─────────┴─────────┐
        ▼                   ▼                           ▼                   ▼
 [ Redis Core Bound ] [ OS / Swap / COW ]        [ Network RTT Latency ] [ Blocking Syscall /
   - Slow commands      - Memory paging            - Packet drops          fsync stall ]
   - O(N) operations    - Fork COW memory          - SYN backlog full    - Disk write stall
   - Large Lua script     exhaustion               - DNS delay           - Slow client buffer
```

---

## 2. Seven-Step Debugging Methodology

### Step 1: Is Redis Responsive at the Network Layer?
Measure raw TCP round-trip latency to the server from the application container/host:
```bash
# redis-cli latency test (samples baseline TCP + event loop delay)
redis-cli --latency -h <host> -p <port>

# Sample with 1-second history graph
redis-cli --latency-history -i 1
```
* **Expected:** $< 1.0\text{ ms}$ (within AWS/GCP region or local network).
* **If $> 20\text{ ms}$:** Network congestion, noisy neighbor VM, or OS TCP backlog exhaustion.

---

### Step 2: What Commands are Slow? (SLOWLOG)
Redis logs every command whose execution time exceeds `slowlog-log-slower-than` (default 10,000 microseconds / 10ms):
```bash
# Check length of slow log
redis-cli SLOWLOG LEN

# Inspect the 10 slowest recent commands
redis-cli SLOWLOG GET 10

# Temporarily lower threshold to 1000 microseconds (1ms) for debugging
redis-cli CONFIG SET slowlog-log-slower-than 1000
```
**Common Culprits:**
* `KEYS *` executed by a dashboard or rogue script ($O(N)$ full keyspace scan).
* `HGETALL` on a hash with $> 100,000$ fields.
* `SMEMBERS` on a set with millions of entries.
* Long-running `EVAL` Lua scripts with complex loops.

---

### Step 3: Is Memory Saturated or Swapping?
Inspect memory metrics directly:
```bash
redis-cli INFO memory
```
Key fields to check:
1. `used_memory_rss`: Physical RAM consumed by the OS process.
2. `mem_fragmentation_ratio`: $\frac{\text{used\_memory\_rss}}{\text{used\_memory}}$.
   * If $> 1.5$: High memory fragmentation. Consider enabling `CONFIG SET activedefrag yes`.
   * If $< 1.0$: **CRITICAL: Redis is swapping to disk!** Swap access causes millisecond disk stalls in the single-threaded loop.
3. `evicted_keys`: If this counter is incrementing rapidly, your working set exceeds `maxmemory`.

---

### Step 4: Is Persistence Blocking the Engine?
Snapshots and AOF writes can cause latency spikes:
```bash
redis-cli INFO persistence
```
* `rdb_last_bgsave_status`: Did the last snapshot fail? (If `stop-writes-on-bgsave-error yes`, writes will be rejected).
* `latest_fork_usec`: Time taken for the kernel to duplicate page tables during `fork()`. On a 32GB instance, fork can freeze the engine for $> 50\text{ ms}$!
* `aof_delayed_fsync`: If the background disk writer is backed up on disk I/O, the main thread will delay writes to prevent memory buffer overflow.

---

### Step 5: Are Clients Misbehaving or Leaking Connections?
Inspect the connected clients:
```bash
redis-cli INFO clients
redis-cli CLIENT LIST
```
Look for:
* `omem` (Output Buffer Memory): If a slow client subscribed to Pub/Sub or ran `MGET` on 50,000 keys, Redis buffers output in memory. If client is slow reading, `omem` balloons.
* `cmd`: Clients stuck on blocking calls (`BLPOP`, `XREAD BLOCK`).

---

### Step 6: Is There a Hot Key?
A single key receiving 50,000 requests/sec can saturate a single Redis thread even if total cluster capacity is huge.
```bash
# Sample keyspace for hot keys (Redis 4.0+)
redis-cli --hotkeys

# Sample keyspace for largest memory consumers
redis-cli --bigkeys
```

---

### Step 7: Latency Monitoring Subsystem
Redis has a built-in latency spike monitor:
```bash
# Enable latency doctor (10ms threshold)
redis-cli CONFIG SET latency-monitor-threshold 10

# Generate automated diagnostic report
redis-cli LATENCY DOCTOR
```
Redis will analyze its internal event loop, fork latency, and slow operations and produce plain-English recommendations.
