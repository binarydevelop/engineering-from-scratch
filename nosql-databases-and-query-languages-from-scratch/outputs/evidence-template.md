# NoSQL Engineering Evidence & Lab Log

## Session Metadata
* **Lesson / Phase:** Phase XX: [Phase Title]
* **Date:** YYYY-MM-DD
* **Database Engine:** [e.g., MongoDB / Apache Cassandra / DynamoDB / Redis / Neo4j / Elasticsearch]
* **Database Version:** [e.g., MongoDB 7.0.12 / Cassandra 5.0.0 / DynamoDB Local 2.5.3]
* **Dataset Used:** [e.g., E-Commerce Orders / Social Graph / IoT Readings / SaaS Events]

---

## 1. Problem & Access Pattern Formulation
* **Business Requirement:** [What exact user request or analytical report are we answering?]
* **Access Pattern ID & Shape:** [e.g., AP-14: Fetch latest 50 messages for conversation ID ordered by timestamp ASC]
* **Query Frequency & Latency SLA:** [e.g., 2,500 QPS, p99 < 10ms]

---

## 2. Hypothesis & Prediction
* **Prediction:** [Before execution: Which partition will be touched? Will the engine use an index or perform a scan? How many records will be examined?]
* **Expected Partitions Touched:** [1 specific partition / Bounded set / All cluster nodes]
* **Expected Index Usage:** [Primary key lookup / Compound index scan / Full table scan]

---

## 3. Data Model & Physical Design
* **Data Model Snippet:**
```text
[Paste DDL, JSON Schema, or Table Definition here]
```
* **Partition Key:** [e.g., `conversation_id`]
* **Clustering / Sort Key:** [e.g., `created_at ASC`]
* **Secondary Indexes:** [e.g., GSI on `sender_id` or Compound Index on `{ customer_id: 1, created_at: -1 }`]

---

## 4. Query Execution & Results
* **Query Statement / Pipeline:**
```text
[Paste exact query or aggregation pipeline here]
```
* **Expected Result:** [Summary or snippet of expected output]
* **Actual Result:** [Summary or snippet of actual output returned]
* **Validation Status:** [ ] PASS   [ ] FAIL

---

## 5. Physical Execution Plan & Metrics
* **Records / Documents Returned:**
* **Records / Documents Examined (if observable):**
* **Index Entries Examined (if observable):**
* **Read Amplification Ratio:** (`Records Examined` ÷ `Records Returned`)
* **Partitions Touched:**
* **Query Plan / Explain Output:**
```json
[Paste explain() or execution plan summary here]
```
* **Execution Latency (p50 / p99):**
* **Throughput (Ops/sec, if measured):**

---

## 6. Deliberate Failure & Debugging
* **What did I intentionally break?** [e.g., Removed clustering index, ran unbounded query, forced ALLOW FILTERING, triggered hot partition]
* **What failed or degraded?** [e.g., Latency spiked 45×, memory exceeded limit, table scan executed]
* **How did I diagnose it?** [e.g., Examined explain("executionStats"), checked nodetool tablehistograms, ran query profiler]
* **Root Cause Classification:**
  - [ ] Query syntax / structure
  - [ ] Missing or suboptimal index
  - [ ] Fundamental data modeling flaw
  - [ ] Bad partition key distribution (hotspot)
  - [ ] Consistency level mismatch / replication lag
  - [ ] Capacity / memory limitation
* **What did I change to fix it?** [e.g., Restructured primary key, created compound index, remodeled as document array]

---

## 7. Comparative Architectural Reflection
* **Would SQL be simpler and safer here?** [Explain trade-offs: Would a normalized PostgreSQL table with an index solve this with fewer compromises?]
* **Would another NoSQL model represent this better?** [e.g., Would a Graph DB be superior to this Wide-Column table, or does Document embedding work best?]
* **Artifact Produced:** [Path to script, query file, or benchmark output in `outputs/`]

---

## 8. Physical Trace in My Own Words
[In 3–5 sentences, explain step-by-step how the database engine routed the request, traversed disk or memory structures, evaluated filters, and assembled the final response.]

---

## 9. Remaining Questions & Next Steps
* [Any unresolved questions regarding storage internals or engine behavior?]
