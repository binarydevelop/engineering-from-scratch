# Phase 266: Azure Cosmos DB: Multi-Model Architecture and the 5 Consistency Levels

## 1. Why This Matters for MAANG & Senior/Staff Roles
Azure Cosmos DB represents Microsoft's flagship globally distributed multi-model database engine. While most engineers treat consistency as a binary choice (Strong vs Eventual in the CAP theorem), Cosmos DB formalized the spectrum of distributed consistency into 5 mathematically defined consistency levels. Understanding this spectrum is critical for senior distributed systems interviews.

---

## 2. Core Concepts & Architecture Deep-Dive
### The 5 Consistency Levels Spectrum
1. **Strong Consistency**:
   - Linearizability. Reads are guaranteed to return the most recent committed version.
   - Cost: Highest latency, reads must query quorum of replicas across regions; cannot write if any replica region is unreachable.
2. **Bounded Staleness**:
   - Reads lag behind writes by a bounded window: either by `K` versions or `T` time (e.g., maximum 5 minutes or 100 updates stale).
   - Ideal for globally distributed systems where slight staleness is acceptable but unbounded lag cannot be tolerated.
3. **Session Consistency (Default - 75% of Production Workloads)**:
   - Read-Your-Own-Writes within a single client session token.
   - If User A updates their profile, User A immediately reads the new profile. Other users in different regions may experience slight eventual consistency delay.
4. **Consistent Prefix**:
   - Updates are never read out of order.
   - If writes occur in order `A -> B -> C`, a reader may see `A`, or `A -> B`, but will *never* see `A -> C` or `B -> A`.
5. **Eventual Consistency**:
   - Weakest consistency. Zero ordering guarantees during concurrent operations.
   - Lowest latency, highest read throughput.

### Multi-Model Storage Internals (Atom-Record-Sequence / ARS)
- Cosmos DB stores all data natively in an internal type system called Atom-Record-Sequence (ARS).
- Protocol projection layers expose ARS through multiple standard APIs:
  - SQL API (Core JSON documents)
  - MongoDB API (Wire-compatible with MongoDB drivers)
  - Cassandra API (CQL wire-compatible)
  - Gremlin API (Graph traversal)
  - Azure Table API (Simple key-value)

### Capacity Model: Request Units (RU/s)
- All database operations (reads, writes, queries, stored procedures) are normalized into **Request Units (RUs)**.
- Reading 1KB item by ID and partition key = 1 RU.
- Writing 1KB item = ~5 RUs.
- Partition key selection is critical: bad partition keys create hot partitions where operations exceed provisioned RU/s, returning HTTP 429 Too Many Requests.

---

## 3. High-Value Interview Angle & Failure Modes
### System Design Interview Application
- **"Compare DynamoDB and Cosmos DB consistency models"**:
  DynamoDB offers only 2 consistency options (Strongly Consistent and Eventually Consistent). Cosmos DB provides a granular spectrum, allowing Session or Bounded Staleness to balance latency, cost, and correctness.
- **"How to avoid HTTP 429 in high-throughput NoSQL architectures?"**:
  Choose high-cardinality partition keys (`userId`, `deviceId`, not `country` or `status`); implement exponential backoff with jitter on client SDKs; use autoscale RU provisioning.

---

## 4. Hands-On Practice & Implementation Drills
Estimate provisioned RU/s required for an application serving 10,000 reads/sec (1KB payload) and 1,000 writes/sec (2KB payload) with Session Consistency.

---

## 5. Key Takeaways & Cheat Sheet
- Cosmos DB provides 5 distinct consistency levels balancing latency, availability, and correctness.
- Session consistency is the optimal default providing read-your-own-writes per user session.
- Normalizes compute and storage into Request Units (RUs).
- Deep knowledge of tunable consistency levels sets Senior/Staff candidates apart in System Design.
