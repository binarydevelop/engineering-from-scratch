# The Canonical System Design Framework

> A disciplined 16-step engineering methodology for designing real-world distributed systems.

---

## The 16 Steps

```text
 1. Clarify requirements
 2. Define scope & non-goals
 3. Identify functional requirements
 4. Identify concrete non-functional requirements
 5. Estimate scale (Numbers & Back-of-the-envelope)
 6. Define API / Interaction contract
 7. Model data & schema
 8. Build the simplest working architecture (One machine)
 9. Identify bottlenecks under load
10. Identify failure modes
11. Scale the measured bottleneck
12. Define consistency expectations
13. Define observability & telemetry
14. Review security & trust boundaries
15. Review infrastructure cost
16. State tradeoffs explicitly
```

---

## Detailed Step Walkthrough

### Step 1: Clarify Requirements
Never jump to architectural solutions before clarifying intent. Ask clarifying questions:
- Who are the users (internal systems, mobile clients, web browsers)?
- What are the core user flows?
- What are the read vs. write expectations?

### Step 2: Define Scope & Non-Goals
Clearly identify what will **not** be designed in this session (e.g. recommendation algorithms, billing integrations).

### Step 3: Functional Requirements
List 2 to 4 mandatory system behaviors (e.g., "User can shorten a URL", "User can retrieve the original URL", "System records click metrics").

### Step 4: Non-Functional Requirements
Avoid hollow buzzwords ("high availability", "fast"). Quantify targets:
- **Availability**: 99.9% vs 99.99% (Annual downtime: 8.76 hrs vs 52.6 mins).
- **Latency**: p99 read < 50ms, p99 write < 200ms.
- **Durability**: Zero data loss for finalized transactions.
- **Consistency**: Strong vs Eventual consistency.

### Step 5: Estimate Scale
Perform back-of-the-envelope calculations:
- DAU $\times$ actions/day = Daily requests.
- Average RPS and Peak RPS ($\times 2.5$).
- Read/Write ratio.
- Inbound and Outbound bandwidth.
- Storage growth per day and over 5 years.
- Cache memory sizing (80/20 rule: cache 20% of daily read data).

### Step 6: Define API Contract
Document clear HTTP/gRPC endpoints with method, path, headers, request bodies, and status codes.

### Step 7: Model Data
Design tables, columns, indexes, and primary key generation schemes (UUID vs Sequential vs Snowflake).

### Step 8: The Simplest Working Architecture
Always begin with **one application server and one database**. This provides the conceptual anchor from which all scaling decisions are justified.

### Step 9: Identify Bottlenecks Under Load
Apply load to the simple architecture and observe what saturates first:
- CPU exhaustion (serialization, encryption)?
- Memory exhaustion (caching, unclosed connections)?
- Disk I/O or IOPS ceiling?
- Database connection pool limits?
- Network bandwidth saturation?

### Step 10: Identify Failure Modes
Enumerate what happens when each component crashes, hangs, or partitions.

### Step 11: Scale the Measured Bottleneck
Add components **only** to alleviate proven bottlenecks:
- Read bottleneck $\to$ Cache-Aside or Read Replicas.
- Write bottleneck $\to$ Sharding, batching, or asynchronous work queues.
- CPU bottleneck $\to$ Multiple application instances behind a load balancer.

### Step 12: Define Consistency Expectations
Address the tradeoffs dictated by the CAP and PACELC theorems:
- Strong consistency (linearizable writes to primary).
- Read-your-writes consistency (sticky routing or reading from primary within TTL).
- Eventual consistency (asynchronous replica propagation).

### Step 13: Observability & Telemetry
Incorporate the three pillars of telemetry:
- **Metrics**: RED method (Rate, Errors, Duration percentiles).
- **Logs**: Structured JSON with correlation IDs.
- **Traces**: Distributed span propagation across RPC/HTTP calls.

### Step 14: Security & Trust Boundaries
- Gateway-level TLS termination, WAF, and rate limiting.
- Cryptographic verification of JWT tokens.
- Least-privilege database roles and encrypted data-at-rest.

### Step 15: Cost Analysis
Evaluate resource economics: compute instances, managed cache cost, storage provisioning, and network egress bandwidth fees.

### Step 16: State Tradeoffs Explicitly
Every architectural decision carries a cost. Document the negative consequences of every choice (e.g. caching introduces memory cost and staleness; sharding introduces cross-shard join complexity).
