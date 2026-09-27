# Mental Models of System Design

System design is intuitive when grounded in fundamental physical, mathematical, and algorithmic principles.

---

## 1. The 7 Justification Questions

Never draw a component in a diagram without answering these seven questions:

```text
1. Why does this exist?
2. What concrete problem appears without it?
3. What does it cost in money, memory, and operational complexity?
4. What new failure mode does it introduce?
5. What assumption does it rely on?
6. How would we know it is failing?
7. What simpler alternative was evaluated and rejected?
```

---

## 2. Little's Law

In any stable queueing system, the average number of concurrent requests ($L$) equals the arrival rate ($\lambda$) multiplied by the average latency ($W$):

$$L = \lambda \times W$$

### Example:
- Arrival rate ($\lambda$): $5,000\text{ req/s}$
- Average latency ($W$): $0.2\text{ s}$ ($200\text{ ms}$)
- Concurrent in-flight requests ($L$): $5,000 \times 0.2 = 1,000\text{ requests}$

### Architectural Consequences:
- If downstream database latency doubles from $200\text{ ms}$ to $400\text{ ms}$, the required connection pool size doubles from $1,000$ to $2,000$ connections.
- If your thread pool or connection pool is capped at $500$, incoming requests will queue, timeout, or drop.

---

## 3. The 4 Golden Signals & RED Method

### RED Method (Request-Driven Services):
- **Rate**: Requests processed per second.
- **Errors**: Number of failing requests (HTTP 5xx, timeouts).
- **Duration**: Latency distribution (specifically p50, p95, p99 percentiles).

### USE Method (Resource-Driven Infrastructure):
- **Utilization**: Percentage of time a resource is busy (CPU, Disk).
- **Saturation**: Degree of queued work awaiting resource service.
- **Errors**: Count of hardware or low-level driver error events.

---

## 4. Latency Numbers Every Systems Engineer Must Know

Approximate physical and networking latencies:

| Operation | Typical Latency | Human Scale (~1s = L1 Cache) |
| :--- | :--- | :--- |
| **L1 CPU Cache Reference** | $0.5\text{ ns}$ | 1 second |
| **Branch Mispredict** | $5\text{ ns}$ | 10 seconds |
| **L2 CPU Cache Reference** | $7\text{ ns}$ | 14 seconds |
| **Mutex Lock / Unlock** | $25\text{ ns}$ | 50 seconds |
| **Main Memory (RAM) Reference** | $100\text{ ns}$ | 3.3 minutes |
| **Compress 1 KB with Zstandard** | $2,000\text{ ns}$ ($2\text{ µs}$) | 1.1 hours |
| **Read 1 MB sequentially from RAM** | $3,000\text{ ns}$ ($3\text{ µs}$) | 1.7 hours |
| **Read 1 MB sequentially from NVMe SSD** | $100,000\text{ ns}$ ($100\text{ µs}$) | 2.3 days |
| **Same-Datacenter Network Roundtrip (RTT)** | $500,000\text{ ns}$ ($0.5\text{ ms}$) | 11.5 days |
| **Read 1 MB sequentially from HDD** | $20,000,000\text{ ns}$ ($20\text{ ms}$) | 1.5 years |
| **Cross-Continent Network Packet (CA to EU)** | $150,000,000\text{ ns}$ ($150\text{ ms}$) | 10.5 years |

---

## 5. CAP vs PACELC Theorem

### CAP Theorem:
Under a network partition ($P$), a distributed system must choose between:
- **Availability ($A$)**: Every non-failing node returns a non-error response (even if stale).
- **Consistency ($C$)**: Every read receives the most recent write or an error.

### PACELC Theorem:
CAP only describes behavior during a partition. PACELC explains regular operation as well:
- **If Partition ($P$)**: Choose between Availability ($A$) and Consistency ($C$).
- **Else ($E$)**: Choose between Latency ($L$) and Consistency ($C$).

```text
PACELC
  ├── If Partition (P)
  │     ├── Availability (A)   (e.g., DynamoDB, Cassandra)
  │     └── Consistency (C)    (e.g., Spanner, Raft)
  └── Else (E)
        ├── Latency (L)        (e.g., MongoDB with unacknowledged writes)
        └── Consistency (C)    (e.g., Relational databases, synchronous replication)
```

---

## 6. ASCII Architecture Paradigms

### Replication:
```text
               writes
                 │
                 ▼
             [Primary]
            /         \
   (async) ▼           ▼ (async)
     [Replica 1]   [Replica 2]
```

### Partitioning / Sharding:
```text
              Key / Hash
                  │
                  ▼
         ┌─────────────────┐
         │ Hash / Modulo N │
         └─────────────────┘
           /       │       \
          ▼        ▼        ▼
       [Shard 0] [Shard 1] [Shard 2]
```

### Caching (Cache-Aside):
```text
[Client] ──▶ [App Server] ──(1. Get Key)──▶ [Cache]
                   │                              │
                   │ (2. Cache Hit: Return)       │
                   ├──────────────────────────────┘
                   │
                   ▼ (3. Cache Miss)
              [Database]
```

### Asynchronous Queue Decoupling:
```text
[HTTP Handler] ──(Fast Ack)──▶ [Client: 202 Accepted]
      │
      ▼
   [Queue] ──▶ [Worker 1] ──▶ [External Service]
           ──▶ [Worker 2]
```
