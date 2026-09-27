# Lesson [Phase Number]: [Descriptive Title]

## Motto
> [State the lesson's core mantra or architectural rule in bold. Example: "Model for the query, not for the entity."]

---

## Problem
[Describe the concrete business or technical scenario. Why are we here? What data is arriving, what user is waiting, or what system is failing?]

---

## Access Pattern
* **Actor / Trigger:** [Who or what is issuing this request?]
* **Frequency:** [Queries per second / Writes per second]
* **Target Latency:** [e.g., p99 < 15ms]
* **Input Keys:** [Which parameters are available at request time? e.g., `customerId`, `timestampRange`]
* **Output Cardinality:** [Single item, bounded list (top 20), unbounded stream?]

---

## Prediction
[Before running any code or writing any query, state your explicit hypothesis. Which partition will this hit? How many records will be scanned? Will the query planner use an index or fallback to a table scan?]

---

## Why This Matters
[Explain why getting this wrong destroys production performance, explodes AWS bills, causes cluster cascading failures, or corrupts downstream reports.]

---

## First Principles
* **Physical Storage Reality:** [How is data laid out on disk or in RAM for this paradigm? e.g., SSTable sorted order, B-tree block, inverted posting list.]
* **Computational Complexity:** [Time complexity: O(1) hash, O(log N) tree search, O(N) linear scan, O(V + E) graph traversal.]
* **Network / Fan-Out Factor:** [Does the coordinator contact 1 partition node or broadcast to all N cluster nodes?]

---

## Mental Model
```text
[Provide an ASCII diagram illustrating the logical and physical data path]
Client Request ──> Partition Key Hash ──> Target Node ──> Primary Index ──> Raw Records
```

---

## Model the Data
[Define the exact schema, document structure, table definition, or graph relationship model. Provide complete JSON, DDL, or CQL code blocks.]

```json
{
  "_comment": "Example schema definition"
}
```

---

## Write the Query
[Write the clean, idiomatic query in the database's native language or query DSL.]

```text
-- Example query code
```

---

## Run It
[Exact command to execute against the local container or simulation environment.]

```bash
# Example execution command
```

---

## Inspect It
[Run `explain()`, execution stats, or query tracing. Record the exact execution plan.]

* **Key / Index Used:**
* **Keys Examined:**
* **Documents / Rows Examined:**
* **Documents / Rows Returned:**
* **Execution Stages:** [e.g., `IXSCAN` ──> `FETCH`]

---

## Measure It
* **Execution Time (p50 / p99):**
* **Read Amplification:** (Records Examined ÷ Records Returned)
* **Payload Size:** (Bytes transferred over wire)

---

## Break It
[Intentionally break the design or query. Run a query that omits the partition key, query an unindexed array, or force an unconstrained full graph traversal.]

---

## Debug It
[Show the error message, the spike in execution latency, or the query planner warning. Walk through the root-cause diagnosis step-by-step.]

---

## Remodel / Reindex
[Remodel the data structure, introduce a compound index, add a clustering column, or invert the relationship to fix the issue.]

```text
-- Remodeled DDL or Index Creation
```

---

## Consistency Implications
* **Write Path Consistency:** [Local quorum, primary-only, background replica sync?]
* **Read Path Consistency:** [Can this read return stale data? What is the maximum replication lag window?]
* **Concurrency Anomalies:** [Lost updates, phantom reads, write skew?]

---

## Scaling Implications
* **At 10× Data:**
* **At 1,000× Data:**
* **Hotspot Risk:** [Can a single customer, celebrity, or device overwhelm one partition?]

---

## When This Database Fits
* [Bullet 1: Workload conditions where this database is the gold standard]
* [Bullet 2: Specific access patterns that align with the physical storage engine]

---

## When It Does Not
* [Bullet 1: Workloads where this choice creates operational misery]
* [Bullet 2: Queries that require ad-hoc joins or broad cross-entity aggregations]

---

## Evidence
[Complete the checklist and link to the output evidence log]
- [ ] Hypothesis verified against actual execution stats
- [ ] `explain` plan captured and documented
- [ ] Failure mode intentionally reproduced and resolved
- [ ] Evidence workbook committed to `outputs/`

---

## Questions for Mastery
1. [In-depth conceptual question testing physical understanding]
2. [Diagnostic question analyzing a slow query trace]
3. [Architectural tradeoff question comparing with relational or alternative NoSQL model]

---

## What Comes Next
[Forward pointer to the next phase and how it builds upon this foundation.]
