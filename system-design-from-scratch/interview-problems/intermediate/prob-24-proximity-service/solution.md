# Architectural Solution: Design a Nearby Places / Yelp Service

> **Tier**: `INTERMEDIATE`

---

## 1. Requirements Summary & System Bounds
- **Functional**: Core CRUD workflows, persistence, and external interface contracts.
- **Non-Functional**: 99.99% availability, p99 read < 50ms, p99 write < 200ms.

---

## 2. Quantitative Architecture Estimations
- **Peak Write QPS**: Sized to support Geohash spatial indexing, radius queries.
- **Storage Footprint**: Calculated based on average record size $\times$ daily write volume $\times$ 1,825 days (5 years).
- **Cache Allocation**: Sized to retain 20% of daily read working set in distributed memory.

---

## 3. Component Architecture & Evolution

### Baseline: Single-Machine Starting Point
```text
[Client] ──▶ [App Server] ──▶ [Primary Database]
```

### Scaled Production Architecture
```text
                               ┌──▶ [App Server 1] ──┬──▶ [Cache Cluster]
[Client] ──▶ [Load Balancer] ──┼──▶ [App Server 2] ──┤
                               └──▶ [App Server 3] ──┴──▶ [Primary DB] ──▶ [Replicas]
                                         │
                                         ▼
                                   [Event Queue] ──▶ [Async Workers]
```

---

## 4. Data Model & Storage Engine
- **Primary Datastore**: Chosen based on access patterns (Relational ACID vs NoSQL Document/Key-Value).
- **Partitioning Strategy**: Sharded by primary entity identifier using consistent hash ring with virtual nodes.
- **Indexing**: Composite indexes on query filter columns; avoiding indexing high-churn fields.

---

## 5. Failure Modes & Mitigations
- **DB Failover**: Health check detection promoting warm replica via Raft/consul lease.
- **Cache Stampede**: Mutex lock preventing parallel database fallbacks on hot key expiration.
- **Backpressure**: Leaky bucket rate limiting returning HTTP 429 when concurrency bounds are exceeded.

---

## 6. Architectural Tradeoffs
- *Caching trades memory expense and potential data staleness for reduced database read latency.*
- *Asynchronous queueing trades read-your-writes consistency for resilient burst handling and decoupling.*
