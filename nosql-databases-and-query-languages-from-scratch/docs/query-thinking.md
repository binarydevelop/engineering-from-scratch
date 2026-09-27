# The 18-Question Query Thinking Framework

Before writing a single line of MQL, CQL, PartiQL, Cypher, or Elasticsearch JSON, an engineer must subject the proposed query to the following 18 physical and architectural questions.

---

### 1. What exact result do I need?
* Define the exact payload shape and fields required by the calling service or client UI.
* *Anti-Pattern:* Requesting the full document or row (`SELECT *`, `{}`) when the caller only needs two fields. Unnecessary projection bloats wire transfer and CPU deserialization.

### 2. What does one stored record / document / node represent?
* Articulate the precise entity or aggregate boundary of a single item in storage.
* *Example:* In MongoDB, does one document represent a single order item, a whole order aggregate with embedded items, or an entire customer account?

### 3. Which access pattern am I serving?
* Match the query to an explicit Access Pattern ID (e.g., `AP-012: Fetch latest 20 notifications for user ordered by timestamp DESC`).
* If the access pattern cannot be described in one concise sentence, the query is likely trying to perform ad-hoc exploration on an operational store.

### 4. Which key identifies the data?
* Identify the exact primary key, partition key, or unique document identifier available in the request context.
* If the key is not available at request time, how does the system locate the record? (Through a secondary index lookup, or worse, a scan?)

### 5. Which partition contains it?
* How does the coordinator node determine which physical node or shard holds the data?
* In hash-partitioned systems, `hash(partition_key) % Ring_Size` dictates the destination. If the partition key is missing from the query, the coordinator must query every partition.

### 6. Can the query target exactly one partition?
* Single-partition queries scale almost linearly with cluster size.
* If the answer is YES, the query has minimal network overhead and bounded tail latency.

### 7. Does the query require multiple partitions (Scatter-Gather)?
* If a query must query $N$ nodes to assemble a result, the request latency is bounded by the slowest replica node (the 99th-percentile tail latency problem).
* Broadcast queries are acceptable for rare analytical tasks, but fatal for high-concurrency OLTP endpoints.

### 8. Is an index involved?
* Identify the exact index name and structure: B-Tree index, SSTable primary index, Local Secondary Index, Global Secondary Index, or Inverted Posting List.
* What are the index bounds? Is it an index seek followed by a range scan, or a full index walk?

### 9. Is the database scanning?
* Check `explain()` output:
  - MongoDB: `COLLSCAN` (Collection Scan) vs `IXSCAN` (Index Scan).
  - Cassandra: Full token ring scan (triggered by `ALLOW FILTERING`).
  - DynamoDB: `Scan` operation vs `Query` operation.
* A scan on a 10,000,000-record dataset under production load will cause thread starvation and disk I/O thrashing.

### 10. Is filtering happening before or after retrieval (Filter-After-Read)?
* In many NoSQL engines (e.g., DynamoDB `FilterExpression` or Cassandra `ALLOW FILTERING`), the engine reads items from disk into memory first, and *then* applies client-specified filter predicates.
* You pay for all records read from disk, even if 99% are discarded before being returned to the client!

### 11. Is sorting supported naturally by physical storage order?
* Does the storage engine return records in the requested order without an in-memory sort buffer?
  - Cassandra / DynamoDB: Supported only if sorting matches the Clustering Key / Sort Key.
  - MongoDB: Supported only if the index covers the sort field (Equality-Sort-Range rule).
  - In-memory sorting (`SORT` stage in Mongo, or `Using filesort` in SQL) will crash or abort if the dataset exceeds the memory buffer threshold (e.g., 100 MB WiredTiger limit).

### 12. Is aggregation required at query time, or should it be precomputed?
* Calculating counts, sums, or distinct sets over millions of documents in an operational store destroys cache locality.
* If a metric (e.g., `total_unread_messages`) is read 10,000× more often than it is written, precompute it on write via atomic increments (`$inc`, `ADD`).

### 13. Is data duplicated specifically for this query?
* NoSQL systems intentionally duplicate data (e.g., duplicating `customer_name` inside `orders_by_customer`) to satisfy queries in a single seek.
* What is the synchronization contract? How does the application maintain consistency when the primary entity is updated?

### 14. Could this query become a hotspot?
* If a single partition key receives 10,000 writes/second (e.g., a flash sale product ID or viral social influencer), that single partition will throttle, causing HTTP 429s or high latency.
* How is write or read sharding applied (e.g., salted keys `PRODUCT#1029#0` to `PRODUCT#1029#9`)?

### 15. What happens when the dataset grows 100×?
* Will this query continue executing in $O(1)$ or $O(\log N)$ time, or does its execution time scale with $O(N)$ total dataset size?
* If latency degrades as the table grows, the design is fundamentally broken.

### 16. What consistency level is expected?
* Does this query require strong consistency (linearizability, `ReadConcern("majority")`, DynamoDB Consistent Read, Cassandra `QUORUM`), or can it accept eventual consistency?
* What happens to user experience if the query returns data that is 250 milliseconds out of date?

### 17. What happens if a replica is stale or recovering?
* If a replica node was offline and recently rejoined, will this query observe an outdated state?
* Is read repair enabled? Will the client read a tombstoned record that has not yet been compacted?

### 18. What is the total computational and network cost of this query?
* Calculate:
  - Disk I/O seeks
  - Read Capacity Units (RCUs) / Keys examined
  - Network payload bytes
  - CPU cycles spent on JSON serialization / regex evaluation / Lucene scoring
* Is this cost justified by the business value of the feature?
