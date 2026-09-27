# System Design Document: [System Name]

> **Canonical System Design Template**
> Use this template for all interview problems, capstones, and architectural reviews.

---

## 1. Clarify Requirements

### Functional Requirements
- What are the core user flows?
- What are the required system inputs and outputs?
- What operations must be supported synchronously vs asynchronously?

### Non-Functional Requirements
- **Availability**: e.g., 99.99% ("four nines" = 52.6 minutes downtime/year).
- **Latency**: e.g., p99 write < 200ms; p99 read < 50ms.
- **Throughput**: Peak requests/sec.
- **Durability**: Zero data loss for committed transactions (RPO = 0).
- **Consistency**: Linearizable, Read-Your-Writes, or Eventual Consistency.

### Out of Scope
- Explicit list of features and edge scenarios excluded from this design.

---

## 2. Estimate Scale (Back-of-the-Envelope)

| Metric | Estimation | Derivation / Formula |
| :--- | :--- | :--- |
| **Daily Active Users (DAU)** | 50M | Product baseline |
| **Requests / User / Day** | 20 | Expected user activity |
| **Total Daily Requests** | 1B | $50\text{M} \times 20$ |
| **Average RPS** | ~11,574 req/s | $1\text{B} / 86,400\text{s}$ |
| **Peak Factor** | 2.5x | Peak traffic multiplier |
| **Peak RPS** | ~28,935 req/s | Average RPS $\times 2.5$ |
| **Read / Write Ratio** | 100:1 | Read-heavy assumption |
| **Read QPS / Write QPS** | 28,650 / 285 | Derived from ratio |
| **Average Payload Size** | 500 bytes | Schema estimate |
| **Storage per Day** | ~14.25 GB | 28.5M writes $\times$ 500 bytes |
| **Storage per 5 Years** | ~26 TB | $14.25\text{ GB/day} \times 365 \times 5$ |
| **Bandwidth (Ingress/Egress)**| ~1.14 MB/s / ~114 MB/s | RPS $\times$ payload size |
| **Cache Memory (20% 1-day)** | ~2.85 GB | 80/20 Pareto rule |

---

## 3. API Contract

```http
POST /v1/records HTTP/1.1
Host: api.system.internal
Authorization: Bearer <token>
Content-Type: application/json
Idempotency-Key: <uuid>

{
  "entity_id": "usr_42",
  "payload": { ... }
}
```

```http
GET /v1/records/{id} HTTP/1.1
Host: api.system.internal
```

---

## 4. Data Model & Schema

```sql
CREATE TABLE records (
    id VARCHAR(64) PRIMARY KEY,
    owner_id VARCHAR(64) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_records_owner ON records (owner_id, created_at DESC);
```

---

## 5. Simplest Architecture (Starting Point)

Always begin with one stateless application server and one database.

```text
[Client] ──▶ [App Server] ──▶ [Primary Database]
```

---

## 6. Read Path
1. Request arrives from client.
2. App queries database for record by ID.
3. Response serialized to JSON and returned.

## 7. Write Path
1. Request validated for required fields.
2. Database transaction opened; row inserted.
3. Transaction committed; HTTP 201 returned.

---

## 8. Bottlenecks Under Scale
- What breaks first?
  - Read traffic saturates single database IOPS and connection pool.
  - App server CPU saturates under concurrent JSON serialization.

---

## 9. Scaling & Evolution

```text
                               ┌──▶ [App Server 1] ──┬──▶ [Cache (Redis)]
[Client] ──▶ [Load Balancer] ──┼──▶ [App Server 2] ──┤
                               └──▶ [App Server 3] ──┴──▶ [Primary DB] ──▶ [Read Replicas]
```

## 10. Caching Strategy
- **Pattern**: Cache-Aside (Lazy loading).
- **Eviction**: LRU with 1-hour TTL.
- **Stampede Defense**: Mutex lock / single-flight loading.

## 11. Asynchronous Work & Queues
- Long-running work (notifications, indexing, external webhooks) decoupled via durable queues.

## 12. Partitioning Strategy
- Sharding key: `hash(owner_id) % N` or Consistent Hash Ring.

## 13. Replication Strategy
- 1 Primary (Writes) with 2 Asynchronous Read Replicas across different Availability Zones.

## 14. Consistency Model
- Primary: Strong consistency.
- Replicas: Eventual consistency with Read-After-Write routing via primary if write occurred within last 5 seconds.

## 15. Failure Modes & Mitigations
- **DB Primary Dies**: Automatic failover to replica; temporary 30s read-only window.
- **Cache Node Dies**: Fall back to read replicas with connection throttling.
- **Worker Crash**: Unacked messages returned to queue visibility timeout.

## 16. Backpressure & Overload
- Token bucket rate limiter at gateway.
- Load shedding rejecting low-priority traffic with HTTP 429 / 503 during CPU > 85%.

## 17. Observability
- RED Metrics: Requests/sec, Error Rate (4xx/5xx), Duration p50/p95/p99.
- Distributed Tracing: W3C `traceparent` context propagated across all service hops.

## 18. Security
- TLS 1.3 in-transit, AES-256 at-rest.
- JWT validation at gateway; scoped RBAC authorization in application logic.

## 19. Cost Analysis
- Compute vs Managed Cache vs Egress bandwidth costs.

## 20. Tradeoffs
- *Cache introduces staleness and eviction complexity.*
- *Read replicas introduce replication lag.*

## 21. Alternative Designs
- *Why not DynamoDB/Cassandra from Day 1? Relational joins and ACID transactions were required during MVP stage.*

## 22. What Changes at 10× Scale?
- Move from single primary DB to horizontally sharded databases with consistent hash ring.

## 23. What Changes at 1/100th Scale?
- Remove Redis cache and read replicas; single $20/month PostgreSQL instance suffices.
