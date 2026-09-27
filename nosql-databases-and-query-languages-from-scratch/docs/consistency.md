# Distributed Consistency, CAP, PACELC & Quorums

In distributed NoSQL architectures, data is replicated across multiple physical machines to ensure high availability and durability. This replication fundamentally alters consistency guarantees.

---

## 1. CAP Theorem: The Rigorous Interpretation

The common adage *"Pick any two of Consistency, Availability, and Partition Tolerance"* is false and dangerous.

```text
You CANNOT "choose" Partition Tolerance.
Network partitions are an unavoidable physical law of distributed networks
(switch failures, cable cuts, packet loss, GC pauses).
```

Therefore, the real choice is: **When a network partition occurs, how does your system behave?**

```text
                        ┌───────────────────────────────┐
                        │   NETWORK PARTITION OCCURS    │
                        └───────┬───────────────┬───────┘
                                │               │
          CP (Consistency / Partition Tolerant) │ AP (Availability / Partition Tolerant)
                                │               │
                                ▼               ▼
     Reject writes or block reads rather        Accept writes and serve reads on both
     than returning stale or divergent state.   sides of the partition, allowing data
     (e.g., MongoDB Primary, HBase, Spanner)    to diverge temporarily.
                                                (e.g., Cassandra default, DynamoDB AP)
```

---

## 2. PACELC Theorem: Beyond Partitions

The CAP theorem only describes behavior *during a rare network partition*. But what happens during the 99.99% of time when the network is completely healthy?

The **PACELC Theorem** (Daniel Abadi) states:
```text
If there is a Partition (P):
    Trade off Availability (A) vs Consistency (C);
Else (E):
    Trade off Latency (L) vs Consistency (C).
```

* **PC/EC (e.g., MongoDB with `w: majority`, PostgreSQL sync replication):** Strong consistency during partitions; trades latency for consistency during normal operations (waits for replica acknowledgments).
* **PA/EL (e.g., Cassandra with `ONE`, DynamoDB default eventual consistency):** High availability during partitions; prioritizes low latency ($< 5\text{ms}$) over consistency during normal operations.

---

## 3. Tunable Quorum Mathematics ($N, R, W$)

In leaderless distributed databases (Cassandra, Dynamo), consistency is configured per-operation using three parameters:

* $N$: Replication Factor (total number of nodes storing a copy of the partition).
* $W$: Write Quorum (number of replicas that must acknowledge a write before success).
* $R$: Read Quorum (number of replicas that must respond to a read before success).

### Strong Consistency Guarantee
$$R + W > N$$

* **Why it works:** By the Pigeonhole Principle, the set of nodes written to ($W$) and the set of nodes read from ($R$) must overlap by at least one node. That overlapping node is guaranteed to possess the latest mutation.
* *Example:* $N = 3, W = 2, R = 2$. $R + W = 4 > 3$. Strong consistency achieved.

### Weak / Eventual Consistency
$$R + W \le N$$

* *Example:* $N = 3, W = 1, R = 1$. $R + W = 2 \le 3$. Fast writes and reads ($< 2\text{ms}$), but reads may return stale data if they contact a replica that has not yet received the write.

---

## 4. Conflict Resolution Strategies

When multiple replicas accept concurrent writes during an AP partition or asynchronous replication, the database must reconcile divergent versions:

### A. Last-Write-Wins (LWW)
* **Mechanism:** The mutation with the highest physical timestamp overwrites previous values.
* **The Fatal Flaw:** Clock drift (NTP synchronization errors, leap seconds) can cause a write that occurred *earlier* in real time to overwrite a write that occurred *later*, silently destroying data!

### B. Vector Clocks / Version Vectors
* **Mechanism:** Each node maintains a vector of logical counters $\langle \text{Node}_A: c_1, \text{Node}_B: c_2 \rangle$. If one vector dominates another component-wise, it causally succeeded it. If neither dominates, a **concurrent conflict** is detected.
* **Resolution:** Passed to the application layer to resolve (e.g., merging shopping cart items).

### C. Conflict-Free Replicated Data Types (CRDTs)
* **Mechanism:** Mathematically formal data structures (PN-Counters, OR-Sets, LWW-Element-Sets) whose merge operations are associative, commutative, and idempotent ($A \lor B = B \lor A$). Conflicts resolve deterministically without central coordination.

---

## 5. Replica Convergence Mechanisms

1. **Read Repair:** During a quorum read ($R \ge 2$), if the coordinator detects that Replica 1 has version $V_2$ while Replica 2 has stale version $V_1$, the coordinator returns $V_2$ to the client and asynchronously issues a background write to update Replica 2.
2. **Hinted Handoff:** If a write targets 3 replicas and Node 3 is temporarily down, the coordinator stores a temporary "hint" on its own disk. When Node 3 comes back online, the coordinator replays the buffered hint.
3. **Anti-Entropy (Merkle Tree Sync):** Background daemons compare cryptographic hashes of key ranges organized as Merkle trees across replicas. Only out-of-sync branches of the tree are streamed over the network, minimizing synchronization bandwidth.
