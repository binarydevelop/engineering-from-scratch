# Phases 101 – 114: Capacity, Overload & Resilience Patterns

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phases 101 – 107: Capacity Modeling, Headroom & Pools

### Capacity Planning Formula (Phase 101)
$$\text{CPU Cores} = \frac{\text{Peak RPS} \times \text{CPU ms / req}}{1000\text{ms}} \times \frac{1}{\text{Target Utilization}}$$
* At 2,500 RPS and 12ms CPU per request:
  - Raw CPU required = $30\text{ cores}$.
  - Sized with 40% headroom (60% utilization target) = $\frac{30}{0.60} = \mathbf{50\text{ cores}}$.

### The Connection Pool Cliff (Phase 105)
When all database connection slots are occupied:
1. Incoming worker threads block in OS `pthread_mutex_lock`.
2. HTTP client connections remain open, buffering in memory.
3. Once the client timeout (e.g. 5s) expires, the client closes the TCP connection, but the server continues waiting for the database!
4. **Fix**: Bounded connection acquisition timeouts (e.g. 250ms) that fail fast.

---

## Phases 108 – 114: Overload Protection & Circuit Breaking

### Load Shedding (Phase 109)
When in-flight concurrency crosses safe capacity:
* **Without Load Shedding**: Latency jumps to 30s for all 1,000 users. 100% of checkouts fail.
* **With Load Shedding**: Reject 100 requests immediately with HTTP 503. The remaining 900 requests finish cleanly in 25ms.

### Retry Storms & Full Jitter (Phase 110)
Uncoordinated retries multiply traffic:
$$\text{Traffic} = \text{Base Traffic} \times (1 + \text{Retries})$$
**The Full Jitter Formula**:
$$\text{Sleep} = \text{random}(0, \min(\text{MaxSleep}, \text{BaseSleep} \times 2^{\text{attempt}}))$$
Jitter disperses retry bursts evenly across the time domain.

### Distributed Deadline Budgets (Phase 111)
If the user's end-to-end timeout is 1.0s:
* Gateway: 1000ms deadline.
* Checkout Service: Receives `Deadline: 950ms` (decremented by gateway latency).
* Payment Service: Receives `Deadline: 800ms`.
* Database Query: Receives `Deadline: 300ms`.
If the deadline has expired, downstream services abort execution immediately rather than doing useless work!

### The Circuit Breaker (Phase 112)
```text
           [ CLOSED ]  ◄── Success Probe ──┐
               │                           │
         Failure Threshold           Cooldown Timer
          (e.g. 5 errors)               (e.g. 15s)
               │                           │
               ▼                           │
            [ OPEN ]  ── Timer Elapses ──► [ HALF-OPEN ]
        (Fails Fast 503)                  (Sends 1 Probe)
```
