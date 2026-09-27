# Capstone 02: Failure-Driven Backend

A resilience and chaos-testing harness for backend systems.
Demonstrates first-principles survival mechanisms:
- **Chaos Injection**: Simulating database drop, cache network partitions, downstream timeouts, and worker panics.
- **Circuit Breaker Pattern**: State machine (`CLOSED`, `OPEN`, `HALF_OPEN`) preventing cascading dependency collapse.
- **Graceful Cache-Aside Degradation**: Transparently falling back to source of truth when Redis/cache fails.
- **Self-Healing Outbox Retries**: Exponential backoff retry policies for background event processing.

---

## 1. Resilience Architecture

```text
Request
   │
   ▼
[Circuit Breaker] ──(Tripped / Open)──▶ [Fallback Response (Fast Fail)]
   │ (Closed)
   ▼
[Cache-Aside Interceptor]
   ├── Cache Hit? ──▶ Return
   └── Cache Failure? ──(Log & Degrade)──▶ [Database Primary]
```

## 2. Failure Scenarios Tested
1. **Cache Partition**: Cache node disappears; system serves requests directly from DB without downtime.
2. **Circuit Tripping**: Consecutive downstream 500s trip circuit breaker to OPEN, shielding downstream dependencies.
3. **Transient Network Flakes**: Outbox worker catches transient HTTP delivery failures and retries with backoff.
4. **Deadline / Timeout Breaches**: Requests exceeding SLA are aborted cleanly.

## 3. Running Tests
```bash
pytest apps/02_failure_driven_backend/tests/ -v
```
