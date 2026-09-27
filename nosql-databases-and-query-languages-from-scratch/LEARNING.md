# The NoSQL Engineering & Query Fluency Learning Guide

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

Welcome to **NoSQL Databases and Query Languages From Scratch**. This curriculum is built on a fundamental realization:

```text
NoSQL is NOT a single database category.
NoSQL does NOT mean "no query language."
NoSQL does NOT mean "faster than SQL."
```

Instead, NoSQL systems represent fundamentally different physical and logical data models—**Document, Wide-Column, Key-Value, Graph, Search, and In-Memory Structures**—each designed around specific access patterns and physical storage realities.

---

## 1. The Core 10-Step Learning Cycle

Every single lesson in this curriculum follows this relentless 10-step pedagogical cycle:

```text
     ┌────────────────────────────────────────────────────────┐
  1. │ REQUIREMENT                                            │
     │ What user action or business process needs data?       │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  2. │ ACCESS PATTERN                                         │
     │ What exact keys, filters, and sort orders are needed?  │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  3. │ MODEL THE DATA                                         │
     │ Design the document, wide-column table, or graph.      │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  4. │ PREDICT                                                │
     │ Predict partition hits, index usage, and scanned items.│
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  5. │ WRITE QUERY                                            │
     │ Formulate the exact native query or pipeline.          │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  6. │ INSPECT                                                │
     │ Run explain(), inspect query plans and stage trees.    │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  7. │ MEASURE                                                │
     │ Measure read amplification (examined vs returned).    │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  8. │ BREAK                                                  │
     │ Intentionally trigger full scans or hot partitions.    │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
  9. │ REMODEL                                                │
     │ Re-index, restructure clustering keys, or duplicate.   │
     └───────────────────────────┬────────────────────────────┘
                                 ▼
     ┌────────────────────────────────────────────────────────┐
 10. │ EXPLAIN                                                │
     │ Articulate the physical storage path in plain terms.   │
     └────────────────────────────────────────────────────────┘
```

---

## 2. The 15 Non-Negotiable Rules of NoSQL Engineering

1. **Identify Access Patterns Before Schema:** In relational databases, you model entities and relationships first, then index queries. In NoSQL, you determine the read and write access patterns first; schema follows access patterns.
2. **Predict the Partition Target:** Before running any query, ask: *Does this query target exactly 1 partition, a known subset, or does it scatter-gather across all nodes in the cluster?*
3. **Write Queries Manually:** Do not hide behind Object-Document Mappers (ODMs) or abstracted libraries. Write raw MQL, CQL, DynamoDB expressions, Cypher, and Elasticsearch JSON.
4. **Inspect the Physical Plan (`explain`):** Never accept a query simply because it returned the expected rows. A query returning 10 rows by examining 10,000,000 documents is a production outage waiting to happen.
5. **Measure Read Amplification:** Compute `Records Examined / Records Returned`. An ideal ratio is 1.0. A ratio > 10.0 signals missing indexes, suboptimal clustering keys, or bad document boundaries.
6. **Understand Write Amplification:** Every secondary index, global index, and replicated copy multiplies write I/O. Indexes are not free; they trade write latency and storage for read performance.
7. **Intentionally Create Bad Partition Keys:** Build skewed partitions (e.g., partitioning IoT events by status instead of device ID) and observe hotspots using tracing tools.
8. **Compare Query Models Across Paradigms:** For every business requirement, evaluate how Document, Wide-Column, Key-Value, Graph, and Search each solve it.
9. **Redesign the Model Instead of Forcing Impossible Queries:** When a query requires `ALLOW FILTERING` in Cassandra or a table `Scan` in DynamoDB, redesign the table or introduce a materialized view instead of bypassing the database's design.
10. **Test Stale Reads & Quantify Lag:** In replicated systems, measure the propagation window where replica nodes serve out-of-date records.
11. **Break Replicas & Test Quorums:** Kill nodes during concurrent reads and writes. Verify mathematically whether `R + W > N` prevents dirty or stale reads.
12. **Avoid Technology-First Decisions:** Never say "We should migrate to Cassandra because it is web-scale." Say "We have a write throughput of 200,000 events/sec with fixed point-in-time access patterns, which matches LSM tree sequential writes."
13. **Always Ask: Would SQL Be Simpler and Safer?** Relational databases with ACID transactions, expressive joins, and foreign keys are the right choice for many workloads. Only choose NoSQL when specific workload characteristics demand it.
14. **Single-Table Design Is an Optimization, Not a Dogma:** DynamoDB single-table design reduces network round trips for high-scale microservices, but adds severe cognitive overhead and schema fragility. Apply it deliberately, not blindly.
15. **Query Syntax Does Not Change Physical Engine Constraints:** Writing SQL-compatible PartiQL over DynamoDB does not give DynamoDB the ability to execute relational joins or cheap ad-hoc aggregations.

---

## 3. The 18-Question Query Thinking Framework

Whenever you formulate any NoSQL query, systematically work through the 18 questions defined in [`docs/query-thinking.md`](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md):

1. What exact result do I need?
2. What does one stored record/document/node represent?
3. Which access pattern am I serving?
4. Which key identifies the data?
5. Which partition contains it?
6. Can the query target one partition?
7. Does it require multiple partitions?
8. Is an index involved?
9. Is the database scanning?
10. Is filtering happening before or after retrieval?
11. Is sorting supported naturally by physical storage order?
12. Is aggregation required at query time or should it be precomputed?
13. Is data duplicated specifically for this query?
14. Could this query become a hotspot?
15. What happens when the dataset grows 100×?
16. What consistency level is expected?
17. What happens if a replica is stale?
18. What is the total computational and network cost of this query?
