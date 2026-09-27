# System Design Tradeoff Map

> "There are no solutions in distributed systems, only tradeoffs." — Thomas Sowell (adapted)

Every architectural decision trades one advantage for another. This map catalogs the primary tradeoffs encountered in modern backend and distributed systems.

---

## 1. Core Architectural Tradeoffs

| Decision / Pattern | Primary Benefit | Architectural Cost / Downside |
| :--- | :--- | :--- |
| **In-Memory Cache (Redis/Memcached)** | Sub-millisecond read latency, shields primary database from read spikes. | Data staleness, memory cost, cache invalidation complexity, stampede failure risk. |
| **Read Replicas** | Scales read throughput horizontally without altering write schema. | Asynchronous replication lag, potential stale reads, increased DB connection management. |
| **Horizontal Sharding** | Overcomes physical single-node storage and write throughput limits. | Complex cross-shard joins, distributed transaction overhead, difficult resharding. |
| **Asynchronous Queues (Kafka/RabbitMQ)** | Decouples producer from consumer, smooths traffic bursts, prevents cascade. | Eventual consistency, asynchronous error handling, consumer lag, poison pill risks. |
| **Microservices Decomposition** | Independent deployments, team scaling, failure containment. | Distributed tracing complexity, network latency overhead, dual-write bugs, network serialization. |
| **Transactional Outbox Pattern** | Guarantees atomic state update and event publishing without 2PC. | Polling latency or CDC agent overhead, duplicate messages under at-least-once delivery. |
| **Consistent Hashing** | Minimizes key remapping when scaling cache or storage nodes ($K/N$ moved). | Non-uniform key distribution without virtual nodes, cascading rebalance load. |
| **Optimistic Locking (Version Column)** | High write throughput when collisions are rare, no blocking DB locks. | High abort and retry rate under heavy write contention on hot records. |
| **Pessimistic Locking (`SELECT FOR UPDATE`)** | Guarantees absolute isolation and prevents race conditions immediately. | Serializes requests, degrades throughput, prone to deadlocks and timeout crashes. |
| **Circuit Breakers** | Prevents failing downstream dependencies from exhausting caller thread pools. | Fast-fails user requests; requires tuning recovery thresholds and fallback mechanisms. |

---

## 2. Consistency vs Availability in Practice

```text
                  LINEARIZABLE CONSISTENCY
                         (Spanner, Raft)
                             ▲
                             │
                             │
       (Strong)              │              (Eventual)
   Reads must reflect        │        High throughput,
   latest global write       │        tolerates network splits
                             │
                             ▼
                    HIGH AVAILABILITY
                 (DynamoDB, Cassandra)
```

- When choosing **Linearizable Consistency**:
  - Writes must acquire distributed quorum or consensus.
  - Latency increases due to cross-node network roundtrips.
  - If a network partition occurs, writes to the minority partition must be rejected.
- When choosing **High Availability**:
  - Writes are accepted locally on any accessible node.
  - Reads may return stale or divergent data.
  - Requires conflict resolution strategies (Last-Write-Wins, Vector Clocks, CRDTs).
