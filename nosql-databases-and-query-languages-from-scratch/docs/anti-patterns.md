# The 17 Fatal NoSQL Anti-Patterns: Architectural Field Guide

This document catalogs the 17 most destructive anti-patterns in NoSQL engineering. For every anti-pattern, we analyze **why it is tempting**, the **exact failure mode**, **how to detect it in telemetry**, the **better design**, and **when it could actually make sense**.

---

### 1. NoSQL Because It Scales
* **Why Tempting:** Resume-driven development, viral blog posts, and the myth that relational databases cannot scale past a few gigabytes.
* **Failure Mode:** Teams abandon relational integrity, ACID transactions, and expressive SQL joins, only to recreate buggy, half-baked transaction managers and join layers in their application code.
* **Detection:** The database has zero partition keys, stores less than 50 GB of data, and spends 80% of application code manually joining IDs across collections.
* **Better Design:** Use modern PostgreSQL or MySQL with connection pooling, read replicas, and proper indexing.
* **When Locally Appropriate:** When write throughput provably exceeds 100,000 writes/sec or the data model is inherently hierarchical/unstructured.

---

### 2. MongoDB as SQL With JSON
* **Why Tempting:** Developers migrate relational tables directly to MongoDB collections, creating 1:1 foreign-key references (`user_id`, `address_id`, `order_id`) without embedding.
* **Failure Mode:** Application issues dozens of consecutive network round-trips or heavy `$lookup` aggregation pipelines per page load, causing latency to explode.
* **Detection:** Mongod profiler shows heavy `$lookup` stages with `TOTAL_KEYS_EXAMINED` orders of magnitude higher than documents returned.
* **Better Design:** Model aggregates by access boundary. Embed 1:1 and bounded 1:N data (e.g., shipping address, line items) directly into the parent document.
* **When Locally Appropriate:** When child entities are massive, updated by independent high-frequency write streams, or referenced by millions of distinct parents.

---

### 3. The Giant Document (Unbounded Arrays)
* **Why Tempting:** Embedding is intuitive: "I'll just push all comments, audit logs, or sensor readings into an array inside the parent document."
* **Failure Mode:** Document grows continuously until hitting MongoDB's 16 MB BSON document limit, WiredTiger cache thrashing, and high write amplification as the whole document is rewritten on disk.
* **Detection:** Document size metrics climbing steadily; queries fetching a 12 MB document just to render a user's display name.
* **Better Design:** The **Bucket Pattern** or Hybrid Reference model: Embed the latest 10 items in the parent document, and store historical items in a separate collection partitioned by parent ID + date bucket.
* **When Locally Appropriate:** Strictly bounded arrays where the maximum cardinality is known and small (e.g., maximum 5 phone numbers or 3 addresses per user).

---

### 4. Cassandra Ad-Hoc Querying
* **Why Tempting:** Engineers assume Cassandra tables can be queried with arbitrary `WHERE` clauses just like relational tables.
* **Failure Mode:** Cassandra rejects queries with non-primary key predicates, prompting the engineer to bypass it using `ALLOW FILTERING`, resulting in full-cluster scans and node crashes.
* **Detection:** System logs filled with `InvalidRequestException` or high read latency alerts across all nodes.
* **Better Design:** Query-first table design. Design a dedicated table for each distinct query pattern (e.g., `orders_by_customer`, `orders_by_status`), duplicating data intentionally.
* **When Locally Appropriate:** Never. Cassandra is explicitly architected around known partition-key lookups.

---

### 5. `ALLOW FILTERING` Everywhere
* **Why Tempting:** Cassandra provides `ALLOW FILTERING` to force the coordinator to scan all partitions when an index or clustering column is missing.
* **Failure Mode:** Works fine in staging with 1,000 rows. In production with 50,000,000 rows, a single query attempts a cluster-wide token ring scan, triggering GC pauses and node timeouts.
* **Detection:** Grepping codebase for `ALLOW FILTERING`; node CPU spikes to 100% on coordinator nodes; `ReadTimeoutException`.
* **Better Design:** Introduce a new table with the appropriate partition/clustering key, or use Storage-Attached Indexes (SAI) in Cassandra 5.0+.
* **When Locally Appropriate:** Ad-hoc operational debugging in staging, or querying a partition where the partition key is already fully specified and the scanned partition has < 100 rows.

---

### 6. DynamoDB Scan as Query
* **Why Tempting:** Calling `scan()` in the AWS SDK is syntactically trivial and avoids thinking about partition keys or Global Secondary Indexes.
* **Failure Mode:** Every single request reads every gigabyte of data across all storage partitions. Read Capacity Units (RCUs) burn out instantly, throttling production traffic and generating thousands of dollars in AWS bills.
* **Detection:** CloudWatch `ConsumedReadCapacityUnits` spikes dramatically; high frequency of `ProvisionedThroughputExceededException`.
* **Better Design:** Always use `Query()` with a specific `PartitionKey` (and optional `SortKey` condition). Create a Global Secondary Index (GSI) if querying by an alternate attribute.
* **When Locally Appropriate:** Offline nightly batch jobs or data export pipelines using parallel segment scans.

---

### 7. Single-Table Design Cargo Cult
* **Why Tempting:** Single-table design in DynamoDB is championed by advanced practitioners as the pinnacle of efficiency.
* **Failure Mode:** Junior teams encode obscure composite keys (`PK=ORG#1#USER#4`, `SK=METADATA#V1`), destroying code readability, preventing ad-hoc inspection, and creating extreme fragility when requirements evolve.
* **Detection:** Engineers unable to explain what data is stored in the table; massive translation layers converting obscure PK/SK strings to domain models.
* **Better Design:** Use multiple tables until a specific high-throughput access pattern proves that single-table co-location is necessary to eliminate multi-table latency.
* **When Locally Appropriate:** High-scale, mature microservices with completely locked-in access patterns requiring sub-10ms point lookups across parent-child entities in a single request.

---

### 8. PartiQL Makes DynamoDB Relational
* **Why Tempting:** PartiQL allows writing `SELECT * FROM Orders WHERE status = 'PENDING'`, making engineers believe DynamoDB now supports relational SQL execution.
* **Failure Mode:** Underneath the SQL syntax, DynamoDB still executes the same physical operations. A `WHERE` clause on an unindexed field triggers a full physical table scan.
* **Detection:** High RCU consumption and slow response times on seemingly simple SQL queries.
* **Better Design:** Ensure PartiQL queries strictly supply the partition key in the `WHERE` clause (`WHERE PK = '...' AND SK = '...'`).
* **When Locally Appropriate:** When standardizing query syntax across polyglot systems, or executing simple point lookups using SQL familiarity.

---

### 9. Graph DB for Ordinary CRUD
* **Why Tempting:** "Everything in the world is connected, therefore our domain is a graph!"
* **Failure Mode:** A team models standard e-commerce orders, line items, and addresses in Neo4j. Transaction throughput crawls, horizontal sharding is virtually impossible, and basic CRUD requires complex Cypher patterns.
* **Detection:** The graph has zero multi-hop traversals or path queries; every query is merely looking up an entity by ID and returning its immediate properties.
* **Better Design:** Use PostgreSQL or MongoDB for transactional CRUD, and project only the relationship graph into Neo4j for network analysis.
* **When Locally Appropriate:** When the primary queries require variable-length path traversal ($A \to B \to C \to D$), shortest paths, or detecting cyclic fraud rings.

---

### 10. Elasticsearch as Primary Transaction Database
* **Why Tempting:** Elasticsearch has rich JSON document APIs, fast search, and dynamic schema creation. Why not use it as the main database?
* **Failure Mode:** Elasticsearch is an inverted search index, not an ACID operational database. It lacks multi-document transactions, has eventual consistency refresh intervals (1 second default), and is vulnerable to split-brain data loss under disk/network strain.
* **Detection:** Support tickets reporting "I just updated my profile, but when I refreshed the page, the old data appeared"; corrupt indices requiring full snapshots restores.
* **Better Design:** Use PostgreSQL or MongoDB as the authoritative Source of Truth, and stream mutations to Elasticsearch via Change Data Capture (CDC) for search only.
* **When Locally Appropriate:** Pure read-only search catalogs, log management, and observability metrics where rare data loss during a cluster crash is acceptable.

---

### 11. Redis as Accidental Source of Truth
* **Why Tempting:** Redis is blazingly fast ($< 1\text{ms}$). Developers start writing primary business data directly into Redis hashes without a persistent backing database.
* **Failure Mode:** A memory spike triggers Redis out-of-memory (OOM) eviction (`volatile-lru` or `allkeys-lru`), silently evicting production customer records. Or a node crash loses seconds of mutations between AOF fsyncs.
* **Detection:** Redis `evicted_keys` metric > 0; data vanishing mysteriously after server restarts.
* **Better Design:** Use Redis strictly as a cache, session store, or rate limiter backed by a durable persistent database (PostgreSQL/MongoDB). If used as a primary store, configure `maxmemory-policy noeviction` and strict AOF `appendfsync always`.
* **When Locally Appropriate:** Ephemeral data that has an explicit expiration date (sessions, auth tokens, rate-limiting tokens).

---

### 12. Secondary Index Everything
* **Why Tempting:** "Let's index every field just in case someone wants to query it later."
* **Failure Mode:** Every write mutation must update the primary table plus all $M$ secondary indexes across disk and network. Write throughput collapses, write amplification spikes 10×, and storage costs double.
* **Detection:** Storage size of indexes exceeds base data size; write latency degrades while read latency is unaffected.
* **Better Design:** Only index fields that match validated, high-frequency access patterns. Use compound indexes following the Equality-Sort-Range (ESR) rule.
* **When Locally Appropriate:** Read-heavy analytical replica nodes where writes are executed in infrequent batch windows.

---

### 13. Random Partition Key
* **Why Tempting:** Using `UUIDv4()` as the partition key guarantees perfectly even distribution across all cluster nodes.
* **Failure Mode:** While writes distribute evenly, no query can ever target a range or group of related items. Every range query or grouped lookup requires a full cluster scatter-gather broadcast.
* **Detection:** Coordinator nodes sending queries to 100% of cluster nodes; tail latency bounded by the slowest cluster node.
* **Better Design:** Use a compound primary key: partition on an entity identifier (e.g., `account_id` or `tenant_id`) and sort by UUID or timestamp within the partition.
* **When Locally Appropriate:** Pure key-value point lookups where items are only ever retrieved individually by their exact random ID.

---

### 14. Time-Only Partition Key
* **Why Tempting:** Partitioning logs or sensor events by `date` or `hour` seems natural for time-series queries.
* **Failure Mode:** All writes for the current minute hit the exact same node/shard in the cluster! The remaining 99 nodes sit completely idle while the current time partition is overwhelmed and crashes.
* **Detection:** Uneven CPU and I/O distribution in monitoring: 1 node at 100% CPU, 19 nodes at 2% CPU.
* **Better Design:** Composite partition key combining an entity hash with a coarse time bucket: `((device_id, date_bucket), timestamp)`.
* **When Locally Appropriate:** Low-throughput batch import jobs where sequential file generation is desired.

---

### 15. One Table Per Entity in Cassandra
* **Why Tempting:** Engineers coming from relational databases create `users`, `orders`, `order_items`, and `products` tables in Cassandra.
* **Failure Mode:** Cassandra cannot perform joins. The application must execute $N+1$ sequential queries across the network to assemble a single screen, resulting in unacceptable page load times.
* **Better Design:** Design tables per query screen. Create `orders_by_customer` and `customer_summary` tables, duplicating fields so the application can render the screen in a single query.
* **When Locally Appropriate:** Pure point-lookup key-value stores where each entity is completely independent.

---

### 16. Eventual Consistency Hand-Waving
* **Why Tempting:** Developers select eventual consistency because "it's faster" without defining what happens when a user reads stale state.
* **Failure Mode:** User transfers money or updates their email address, immediately refreshes the page, and sees the old email or old balance. Frustrated users submit duplicate transactions or chargebacks.
* **Detection:** User bug reports claiming actions "didn't save"; duplicate submissions in databases.
* **Better Design:** Implement Read-Your-Writes consistency: read from the primary/leader node or use causal consistency sessions for the mutating user, while serving background reads from eventual replicas.
* **When Locally Appropriate:** Social media like counters, view counts, product review aggregations, and metrics dashboards where sub-second staleness causes zero business harm.

---

### 17. Polyglot Persistence Everywhere
* **Why Tempting:** Using MongoDB, Cassandra, Redis, Neo4j, and Elasticsearch all in the same small application sounds like cutting-edge architecture.
* **Failure Mode:** Operational nightmare. Small engineering teams spend all their time managing backups, schema migrations, cross-database sync pipelines, dual writes, and cluster upgrades across five distinct database engines.
* **Detection:** More time spent debugging CDC pipeline sync lags than writing business features; team cannot explain how data consistency is recovered after a crash.
* **Better Design:** Start with a single robust database (such as PostgreSQL with JSONB and pgvector, or MongoDB). Only extract a specialized store when a proven performance bottleneck emerges.
* **When Locally Appropriate:** Large enterprises with dedicated platform infrastructure teams supporting distinct microservices with validated scale boundaries.
