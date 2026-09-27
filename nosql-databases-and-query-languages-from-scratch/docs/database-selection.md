# Database Selection Framework & Tradeoff Matrix

> **Core Rule:** Never rank databases universally. The correct database is strictly a function of workload characteristics, access patterns, consistency requirements, and organizational operational expertise.

---

## 1. Multi-Paradigm Comparison Matrix

| Workload Dimension | Relational (PostgreSQL) | Document (MongoDB) | Wide-Column (Cassandra) | Cloud KV/Doc (DynamoDB) | In-Memory (Redis) | Property Graph (Neo4j) | Search Index (Elasticsearch) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Data Model** | Tables, Rows, Relations | BSON Hierarchical Documents | Partitioned Rows & Columns | Key-Value / Sparse Document | In-Memory Data Structures | Nodes, Relationships, Properties | Inverted Index / Documents |
| **Storage Engine** | Heap + B-Tree Indexes | WiredTiger B-Tree | LSM Tree (Memtable + SSTables) | Distributed Partitioned B-Tree | RAM (AOF / RDB persistence) | Direct Pointer Adjacency | Lucene Segments (Inverted Index) |
| **Query Language** | SQL (ANSI Standard) | MQL & Aggregation Pipeline | CQL (SQL-like subset) | Native API & PartiQL subset | Redis Commands & RedisSearch | Cypher (GQL aligned) | JSON Query DSL |
| **Write Throughput** | Moderate (10k-50k/sec) | Moderate-High (50k-150k/sec) | Extreme (500k-2M+/sec) | High (Auto-scaled provisioned) | Extreme (100k-1M+/sec single node)| Low-Moderate (10k-50k/sec) | Moderate (batch indexing) |
| **Ad-Hoc Query Flexibility**| **Highest** (Arbitrary joins/filters) | **High** (Nested queries, $lookup) | **Very Low** (Must match key model) | **Low** (KeyCondition + GSIs) | **Very Low** (Key lookup, structures)| **High for Paths** (Graph patterns) | **Highest for Text** (Fuzzy, terms) |
| **Relationship Traversal** | Expensive joins ($O(N \log M)$) | $O(N)$ lookup or embed | Unsuited (No joins) | Unsuited (Adjacency list hacks)| Unsuited (Manual sets) | **Native Pointer Hop** ($O(1)$) | Unsuited (Parent/Child nested) |
| **Consistency Default** | Strong ACID (Serial / Read Comm) | Strong (Primary) / Causally Cons | Tunable Quorum ($R+W > N$) | Eventual (Strong opt-in) | Single-node linear / Async Repl | Strong ACID (Single instance) | Near real-time (Refresh interval) |
| **Scaling Mechanism** | Vertical + Read Replicas | Sharded Clusters | Peer-to-Peer Ring (Masterless) | Fully Managed Cloud Sharding | Redis Cluster (Hash slots) | Vertical + Causal Clustering | Distributed Sharded Cluster |
| **Operational Overhead** | Low to Moderate | Moderate | High (Compaction, repair, JVM) | Zero (Serverless / Managed) | Low | Moderate | High (JVM tuning, GC, segments) |

---

## 2. Decision Tree for Database Selection

```text
Do you have complex ad-hoc queries, multi-table transactions, and strict foreign keys?
   ├── YES ──► POSTGRESQL / RELATIONAL DATABASE (Stop here; do NOT force NoSQL!)
   └── NO
        │
        Is full-text fuzzy matching, relevance ranking, or faceted search the core workload?
        ├── YES ──► ELASTICSEARCH / OPENSEARCH
        └── NO
             │
             Are multi-hop relationship traversals (fraud rings, social graphs, shortest path) dominating?
             ├── YES ──► NEO4J / PROPERTY GRAPH
             └── NO
                  │
                  Is ultra-low latency (< 1ms) caching, rate limiting, or ranking leaderboards required?
                  ├── YES ──► REDIS
                  └── NO
                       │
                       Is the write volume massive (> 200,000 writes/sec) with strict, predefined query paths?
                       ├── YES ──► APACHE CASSANDRA / SCYLLADB
                       └── NO
                            │
                            Do you require serverless zero-maintenance key/range queries with predictable latency?
                            ├── YES ──► AMAZON DYNAMODB
                            └── NO  ──► MONGODB (Hierarchical documents, evolving schemas, rich aggregation)
```

---

## 3. When SQL Is the Superior Choice (Do NOT Force NoSQL)

Engineers frequently introduce NoSQL under the false belief that "SQL doesn't scale." This is an amateur anti-pattern. Modern PostgreSQL easily handles tens of terabytes of data and hundreds of thousands of queries per second on standard hardware.

### Choose SQL When:
1. **Ad-Hoc Reporting & Analytics:** Business analysts need to write unpredictable queries joining multiple business dimensions (`WHERE orders.created_at > ... JOIN customers JOIN promotions`).
2. **Strict Multi-Entity Financial Invariants:** Transferring money between account $A$ and account $B$ where atomicity, isolation, and foreign key constraints are non-negotiable.
3. **Data Shape Is Naturally Tabular & Normalized:** Clear one-to-one and one-to-many relationships without deeply nested variable trees.
4. **Early-Stage Startups & Ambiguous Products:** When access patterns are not yet locked in. In a relational database, you can create a new index tomorrow to support a new query. In wide-column stores, a new query pattern may require backfilling an entirely new table.

---

## 4. The Polyglot Persistence Pattern

In modern production systems, complex applications rarely rely on a single database. Instead, they compose specialized engines around an authoritative **Source of Truth**:

```text
                     ┌───────────────────────────────┐
                     │          CLIENT APP           │
                     └───────┬───────────────┬───────┘
                             │               │
                     Writes  │        Reads  │
                             ▼               ▼
                   ┌───────────────────┐   ┌───────────────────┐
                   │    PostgreSQL     │   │       Redis       │
                   │ (Source of Truth) │   │ (Sub-ms Hot Cache)│
                   └─────────┬─────────┘   └───────────────────┘
                             │
                  Change Data│ Capture (CDC)
                  (e.g., Debezium / Kafka)
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   ┌─────────────────┐               ┌─────────────────┐
   │  Elasticsearch  │               │      Neo4j      │
   │  (Search Index) │               │  (Fraud Graph)  │
   └─────────────────┘               └─────────────────┘
```

* **Core Discipline:** Always designate exactly **one** database as the authoritative Source of Truth (typically PostgreSQL or MongoDB). All other databases (Elasticsearch, Redis, Neo4j) are derived secondary projections synchronized via event streams. If a derived store corrupts, it can be re-indexed from scratch without data loss.
