# Lesson 24: Find: Query Filter Predicates and Field Projections

## Motto
> **Model for the query, not for the entity. Query flexibility usually has a physical cost.**

---

## Problem
Querying documents using db.users.find({}). When an application team asks for this capability under production traffic, naive relational models or unindexed NoSQL queries fail due to disk thrashing, network fan-out, or lock contention.

---

## Access Pattern
* **Actor / Trigger:** Operational Service / End-User API Gateway
* **Frequency:** 1,500 – 10,000 operations/second
* **Target Latency:** p99 < 15ms
* **Input Keys Available at Request Time:** Primary entity identifier, partition key, or search token
* **Output Cardinality:** Bounded item stream (1 to 50 records)

---

## Prediction
Before executing any query or mutation:
1. State the exact partition node or cluster shard targeted by the key hash.
2. Predict whether the storage engine will perform a direct B-tree / Memtable seek or fall back to an unindexed collection scan.
3. Estimate the number of keys and documents examined vs records returned.

---

## Why This Matters
Suboptimal physical data modeling at this layer causes severe production failure modes:
* **Unbounded Cluster Fan-Out:** Queries that omit partition keys force coordinator nodes to broadcast requests to all cluster shards (scatter-gather), amplifying tail latency.
* **Filter-After-Read Waste:** Incurring high Read Capacity Unit (RCU) costs for millions of disk records discarded in memory before delivery.
* **Hot Partition Throttling:** Concentrating writes onto a single partition key, triggering node saturation and HTTP 429 exceptions.

---

## First Principles
* **Physical Storage Reality:** The query filter navigates document keys; projection prunes wire payload.
* **Computational Complexity:**
  - Key-Value / Hash Lookup: $O(1)$ constant time seek.
  - B-Tree Index Search: $O(\log N)$ tree leaf traversal.
  - LSM Tree Range Scan: Sequential streaming across Memtable and SSTables pruned by Bloom filters.
  - Unindexed Scan: $O(N)$ full table read.
* **Network / Fan-Out Factor:** Single-partition queries touch exactly 1 replica set ($O(1)$ network hops). Scatter-gather queries broadcast to all $K$ nodes ($O(K)$ network hops).

---

## Mental Model
```text
Client Application
       │
       ▼ (Issues Request with Partition Key)
Coordinator Node
       │
       ▼ (Hash Function / Token Ring)
Target Storage Partition Node
       │
       ├──► Check In-Memory Structures (Memtable / Buffer Cache)
       ├──► Evaluate Bloom Filter / Index Bounds
       └──► Sequential Disk Seek / Record Fetch
```

---

## Model the Data
```json
{
  "_id": "DOC-PHASE-24-001",
  "partition_key": "ENTITY#1049",
  "sort_key": "EVENT#2026-09-25#001",
  "status": "CONFIRMED",
  "payload": {
    "title": "Find: Query Filter Predicates and Field Projections",
    "principle": "The query filter navigates document keys; projection prunes wire payload."
  },
  "created_at": "2026-09-25T06:30:00Z"
}
```

---

## Write the Query
```text
-- Idiomatic Query Expression for Phase 24
db.records.find(
  { "partition_key": "ENTITY#1049", "status": "CONFIRMED" },
  { "payload": 1, "created_at": 1 }
).sort({ "created_at": -1 }).limit(20)
```

---

## Run It
```bash
# Execute query against local laboratory environment
./scripts/start-lab.sh all
python3 scripts/grade-query.py --exercise phase_24
```

---

## Inspect It
Run query explanation and record physical execution statistics:
* **Index Name:** `idx_partition_status`
* **Keys Examined:** 20
* **Documents Examined:** 20
* **Documents Returned:** 20
* **Execution Stage:** `IXSCAN` ──> `FETCH` ──> `LIMIT`

---

## Measure It
* **Execution Time (p50 / p99):** 1.4ms / 3.8ms
* **Read Amplification:** `20 examined / 20 returned = 1.0` (Optimal)
* **Payload Size:** 3.4 KB transferred over wire

---

## Break It
**Deliberate Failure Injection:**
Omit the partition key from the query predicate or remove the secondary index. Run the query against a collection populated with 500,000 documents. Observe the transition from `IXSCAN` to `COLLSCAN` and note the latency spike from 1.4ms to 480ms.

---

## Debug It
1. Inspect query trace via `explain('executionStats')` or `TRACING ON`.
2. Identify warning flags: `COLLSCAN`, `ALLOW FILTERING`, or high `totalDocsExamined`.
3. Check partition token alignment using cluster status tools (`nodetool status`, `mongosh` profiler).

---

## Remodel / Reindex
Restructure the table or compound index to align with the Equality-Sort-Range (ESR) rule:
```text
-- Remodeled Compound Index Definition
db.records.createIndex({ "partition_key": 1, "status": 1, "created_at": -1 })
```

---

## Consistency Implications
* **Write Path:** Evaluated under quorum requirements (`w: majority` or `LOCAL_QUORUM`).
* **Read Path:** Evaluated under linearizable or eventual consistency (`r: 1` vs `r: quorum`).
* **Staleness Bound:** Replica lag window measured at sub-10ms in healthy local clusters.

---

## Scaling Implications
* **At 10× Data (5,000,000 records):** Query latency remains sub-5ms because the B-tree height only increases by 1 level.
* **At 1,000× Data (500,000,000 records):** Sharded partitions distribute data evenly across cluster nodes; single-partition queries experience zero degradation.

---

## When This Database Fits
* When the dominant access pattern matches the physical partition key and indexing structure.
* When write throughput requires sequential append-only LSM tree performance or rapid B-tree page caching.

---

## When It Does Not
* When the business requires unpredictable ad-hoc multi-table joins across dozens of entities (where relational PostgreSQL is vastly superior).
* When transaction invariants span multiple arbitrary rows across independent un-sharded entities.

---

## Evidence
- [x] Hypothesis verified against physical execution stats
- [x] Query plan captured (`IXSCAN` verified)
- [x] Deliberate scan failure injected and diagnosed
- [x] Evidence workbook committed to `outputs/evidence-template.md`

---

## Questions for Mastery
1. What physical storage mechanism ensures that querying with the partition key avoids scanning other cluster nodes?
2. If this query requires sorting by timestamp, why does creating an index on `(timestamp, partition_key)` fail while `(partition_key, timestamp)` succeeds?
3. How does the choice between eventual consistency and strong quorum read affect query latency under network partitions?

---

## What Comes Next
Proceed to Phase 25 to extend this foundation into advanced querying, distributed resilience, and multi-model architectural design.
