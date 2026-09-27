# The NoSQL Database & Distributed Storage Glossary

This glossary provides authoritative, first-principles definitions for key concepts in NoSQL databases, storage engines, distributed consistency, and query models.

---

### Access Pattern
The specific manner in which an application requests data, defined by the parameters available at query time, the required filter conditions, sorting orders, read/write frequency, and latency SLAs. In NoSQL systems, schema is derived directly from access patterns rather than abstract entity normalization.

### Bloom Filter
A space-efficient, probabilistic data structure used in LSM tree storage engines (such as Cassandra and RocksDB) to test whether an element is a member of a set. False positives are possible, but false negatives are impossible. It prevents expensive, unnecessary disk seeks into SSTables that do not contain the requested key.

### Clustering Key / Sort Key
In wide-column (Cassandra) and partitioned key-value (DynamoDB) databases, the portion of the primary key that determines the physical on-disk sort order of rows within a single partition. Enables sequential, single-seek range queries within a partition.

### Compaction
In Log-Structured Merge-tree (LSM) architectures, the background process that merges multiple immutable sorted string tables (SSTables), discards overwritten values and tombstones, and outputs a consolidated new SSTable. Traded off against write and space amplification.

### Consistent Hashing
A distributed partitioning technique where both nodes and data keys are mapped onto a logical circular ring ($[0, 2^{32}-1]$). When a node is added or removed, only $K/N$ keys need to be remapped (where $K$ is total keys and $N$ is total nodes), avoiding cluster-wide re-shuffling.

### Document Aggregate Boundary
In document databases (MongoDB), the boundary enclosing data that is frequently created, read, and updated together as a single atomic unit. Governs decisions regarding when to embed child entities versus when to reference them.

### Fan-Out / Scatter-Gather
A distributed query pattern where the coordinator node must broadcast the query to multiple (or all) partitions in a cluster because the query predicate does not specify the partition key. Highly susceptible to tail-latency amplification (the slowest node dictates overall latency).

### Global Secondary Index (GSI)
An index partitioned on an attribute different from the base table's partition key. In DynamoDB and wide-column stores, GSIs maintain an asynchronous, eventually-consistent secondary partition mapping to serve alternative query access patterns.

### Hot Partition / Hot Key
A failure mode in distributed databases where an disproportionate volume of read or write traffic targets a single partition key (e.g., a viral post or high-volume device), overwhelming the specific node or shard hosting that key while other nodes remain idle.

### Inverted Index
The core storage structure behind full-text search engines (Elasticsearch, Apache Lucene). Maps individual tokens/terms to a posting list of document IDs containing that term, along with term frequencies and positional offsets.

### Log-Structured Merge-Tree (LSM Tree)
A storage engine architecture optimized for high write throughput. Writes are appended sequentially to an in-memory sorted structure (`Memtable`) and write-ahead log (`WAL`). When the memtable fills, it is flushed sequentially to disk as an immutable `SSTable`. Reads check the memtable and SSTables, using Bloom filters to prune disk searches.

### Memtable
The volatile, in-memory write buffer of an LSM tree (typically implemented as a SkipList or Red-Black Tree) where mutations are buffered in sorted key order before being written to disk as an immutable SSTable.

### Partition Key / Shard Key
The attribute used by a distributed database's hash function to assign a record to a specific physical node or partition. Determines data locality; all items with the exact same partition key reside on the same partition.

### Polyglot Persistence
The architectural practice of utilizing different database technologies within a single software architecture, choosing each storage engine (e.g., PostgreSQL for transactions, Redis for caching, Elasticsearch for search, Neo4j for fraud graphs) based on specific access pattern requirements.

### Quorum ($N, R, W$)
In leaderless distributed databases (Cassandra, Dynamo), the replication parameters governing read and write consistency. $N$ is the replication factor, $W$ is the number of replicas that must acknowledge a write, and $R$ is the number of replicas that must respond to a read. When $R + W > N$, the system guarantees that the read set and write set overlap on at least one replica node.

### Read Amplification
The ratio of physical bytes or records read from storage/memory to the logical bytes or records actually requested by the client. High read amplification indicates table scans, inefficient indexes, or large tombstones.

### Read Repair
In distributed leaderless stores, an optimization where a client or coordinator issuing a quorum read detects version mismatches among replicas and asynchronously pushes the most recent value to the out-of-date replica nodes.

### SSTable (Sorted String Table)
An immutable on-disk file format storing key-value pairs sorted strictly by key. Because SSTables are immutable, writes require no random in-place updates; deletes are recorded via tombstones.

### Tombstone
A marker written to an append-only or immutable storage system (such as an LSM tree) indicating that a key has been deleted. The tombstone suppresses the deleted record during reads until background compaction physically removes both the tombstone and the underlying expired data.

### Two-Way vs One-Way Door Schema Decisions
A schema decision is a *two-way door* if adding an optional field or secondary index can be easily rolled back or modified online. It is a *one-way door* if changing a partition key on a 50-terabyte table requires a full re-sharding and data migration.

### Vector Clock
An algorithm for generating logical timestamps across distributed nodes without synchronized physical clocks, capturing causal relationships (happened-before) between events to detect concurrent conflicting writes.

### Write Amplification
The ratio of bytes written to persistent non-volatile storage (disk/SSD) relative to the logical bytes submitted in the client's write request. Amplification is driven by WAL logging, memtable flushing, LSM tree compactions, and secondary index maintenance.
