# NoSQL Mental Models & Physical Storage Realities

> **Core Principle:** Query flexibility usually has a physical cost.

When engineers ask *"Which NoSQL database is best?"*, they are asking the wrong question. Databases are physical engines that store bytes on disk, buffer pages in RAM, and transmit frames over network switches. Different data structures optimize for fundamentally different operations.

---

## 1. The Fundamental Tradeoff: Query Flexibility vs Physical Predictability

```text
▲ High
│                                       Relational (PostgreSQL)
│                                       • Ad-hoc joins, arbitrary WHERE, rich indexes
│                                       • Query planner picks execution paths dynamically
│                                       • High flexibility; latency depends on plan
│
│                 Document (MongoDB)
│                 • Rich nested queries, aggregation pipeline
│                 • Secondary indexes, schema flexibility
│                 • B-Tree storage; bounded joins via $lookup
│
│                                       Search / Inverted Index (Elasticsearch)
Q                                       • Full-text relevance, token matching, faceting
U                                       • Segment merges, memory intensive
E
R
Y                 Wide-Column (Cassandra)
│                 • Fixed query paths defined by partition + clustering key
F                 • Append-only LSM Trees, extreme sequential write throughput
L                 • No ad-hoc joins, queries must specify partition key
E
X                 Key-Value (DynamoDB / Redis)
I                 • O(1) targeted hash lookups, rigid point/range access
B                 • Constant predictable latency at petabyte scale
│                 • Query shape strictly dictates schema
▼ Low
  └────────────────────────────────────────────────────────────────────────►
   Low                   Physical Predictability & Scale Boundary       High
```

---

## 2. The Five Physical Storage Engines

### A. B-Tree Storage Engines (e.g., WiredTiger in MongoDB)
* **Structure:** Multi-way balanced search trees storing ordered key-value pairs or document records in fixed-size pages (typically 4 KB or 32 KB).
* **Write Mechanism:** In-place page updates with Write-Ahead Logging (WAL) for crash durability. Updates to non-contiguous keys cause random I/O writes.
* **Read Mechanism:** $O(\log N)$ logarithmic tree traversal to locate the specific leaf page, followed by in-memory scanning.
* **Optimal Workload:** Mixed read/write workloads with localized point lookups, bounded range queries, and document updates where document size does not dramatically expand.

### B. Log-Structured Merge-Tree (LSM Tree) (e.g., Apache Cassandra, ScyllaDB)
* **Structure:** In-memory sorted buffer (`Memtable`) + append-only disk commit log + cascade of immutable sorted disk files (`SSTables`).
* **Write Mechanism:** Writes append sequentially to the commit log and insert into the in-memory Memtable ($O(\log M)$). Zero random disk seeks during writes! Sequential throughput reaches the physical bus limit.
* **Read Mechanism:** Must check the Memtable, followed by checking multiple SSTables from newest to oldest. Probabilistic Bloom filters prevent checking SSTables that do not contain the key.
* **Compaction:** Background threads merge sorted SSTables to reclaim space from tombstones and overwritten keys.
* **Optimal Workload:** Extremely high-throughput write streams (time-series, logs, financial transactions, telemetry) where queries are partitioned by known keys.

### C. Inverted Index Storage Engines (e.g., Apache Lucene in Elasticsearch)
* **Structure:** Lexicon of indexed terms mapped to sorted posting lists containing document IDs, term frequencies, and character offsets.
* **Write Mechanism:** Documents are tokenized by text analyzers and written to immutable segment files. Periodic segment merges consolidate postings.
* **Read Mechanism:** Multiple term posting lists are intersected using bitset operations to evaluate boolean combinations (`MUST`, `SHOULD`, `FILTER`).
* **Optimal Workload:** Full-text discovery, relevance ranking, prefix search, and multi-dimensional faceted filtering across billions of text records.

### D. Native Property Graph Engines (e.g., Neo4j)
* **Structure:** Index-free adjacency. Nodes and relationships are stored as direct physical pointer records on disk.
* **Traversal Mechanism:** Following an edge from Node $A$ to Node $B$ is a pointer dereference ($O(1)$ per edge), rather than an index scan or relational table join ($O(N \log M)$).
* **Optimal Workload:** Highly interconnected data where the query involves multi-hop traversals, shortest path calculations, fraud rings, or network dependency graphs.

### E. In-Memory Structured Engines (e.g., Redis)
* **Structure:** RAM-resident hash tables, skip lists, radix trees, and zip lists.
* **Execution Mechanism:** Single-threaded or multiplexed event loop executing commands directly against CPU cache-resident memory. Optional asynchronous snapshotting (RDB) and append-only file (AOF) persistence.
* **Optimal Workload:** Sub-millisecond caches, session states, real-time leaderboards, rate limiters, and atomic counter synchronization.

---

## 3. Physical Query Execution Traces

### Trace 1: MongoDB Point & Filter Query
```text
Client: db.users.find({ country: "DE", age: { $gte: 25 } })
   │
   ▼
1. Query Optimizer matches Compound Index: { country: 1, age: 1 }
   │
   ▼
2. Index Scan (IXSCAN): Seeks B-Tree node for "DE", walks contiguous leaf entries where age >= 25
   │
   ▼
3. Document Fetch (FETCH): Dereferences RecordIDs from index to read actual BSON documents from WiredTiger cache
   │
   ▼
4. Network: Returns filtered document stream to mongosh / application
```

### Trace 2: Apache Cassandra Partitioned Read
```text
Client: SELECT * FROM sensor_readings WHERE device_id = 'DEV-99' AND ts >= '2026-09-25';
   │
   ▼
1. Coordinator Node hashes device_id using Murmur3Partitioner: hash('DEV-99') = -42981048120
   │
   ▼
2. Coordinator routes request directly to the replica nodes responsible for that token range
   │
   ▼
3. Target Node checks Memtable for 'DEV-99'
   │
   ▼
4. Target Node evaluates Bloom Filters on disk SSTables (skips 90% of files)
   │
   ▼
5. SSTables containing partition are read; rows are sequentially read using clustering column order (ts >= 2026-09-25)
   │
   ▼
6. Coordinator merges responses according to Consistency Level (e.g., LOCAL_QUORUM) and returns to client
```

### Trace 3: Amazon DynamoDB Query vs Scan
```text
Targeted Query:
PK = "USER#42", SK begins_with("ORDER#")
   │
   ▼
Hash(PK) maps to exact storage partition partition_4.
Engine seeks to first item matching "ORDER#" in B-tree partition file.
Reads sequential items until prefix terminates.
Returns exact requested items. (RCU cost = size of items returned)

Table Scan:
Scan(FilterExpression: status = "SHIPPED")
   │
   ▼
Engine MUST read every single physical partition in the entire table.
Reads 100,000 items from disk.
Discards 99,950 items in memory because status != "SHIPPED".
Returns 50 items. (RCU cost = charged for ALL 100,000 items read!)
```

### Trace 4: Neo4j Graph Traversal
```text
Client: MATCH (p:Person {id: 'u1'})-[:FRIEND]->(f)-[:FRIEND]->(fof) RETURN fof.name
   │
   ▼
1. Schema Index lookup locates starting Node pointer for 'u1' (one-time index seek)
   │
   ▼
2. Traversal Engine follows physical doubly-linked pointer chain of [:FRIEND] relationships directly on disk record
   │
   ▼
3. For each friend Node pointer, engine immediately traverses their [:FRIEND] relationship chain
   │
   ▼
4. Zero table scans, zero hash joins. Traversal speed is independent of total graph size.
```

### Trace 5: Elasticsearch Boolean Query
```text
Client: { "query": { "bool": { "must": { "match": { "title": "noise cancelling" } }, "filter": { "term": { "status": "active" } } } } }
   │
   ▼
1. Filter Context: "status": "active" retrieves pre-cached BitSet from segment memory (0 score calculation)
   │
   ▼
2. Query Context: Analyzers tokenize "noise cancelling" ──> terms ["noise", "cancelling"]
   │
   ▼
3. Lucene looks up terms in Inverted Index Lexicon; retrieves posting lists for both terms
   │
   ▼
4. Posting lists are intersected with the status BitSet using skip lists
   │
   ▼
5. BM25 relevance score is calculated ONLY for surviving candidate documents
   │
   ▼
6. Top K scored results are sorted and returned
```
