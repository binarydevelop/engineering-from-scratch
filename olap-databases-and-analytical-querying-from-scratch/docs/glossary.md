# The Definitive OLAP & Analytical Systems Glossary

This glossary defines the foundational concepts of analytical database engineering, columnar storage, vectorized execution, and distributed analytical query engines.

---

## 1. Relational & Analytical Modeling

### Grain
The atomic level of detail represented by exactly one row in a table. Defining the grain is the non-negotiable first step in data modeling. Examples: "one line item inside an e-commerce order", "one HTTP request processed by an edge proxy", or "one 1-minute aggregated metrics snapshot for a CPU core".

### Dimension
A qualitative, categorical, or temporal attribute that provides context to an analytical event (e.g., `country`, `device_type`, `campaign_id`, `event_date`). Dimensions are used for filtering (`WHERE`), slicing (`CASE`), and grouping (`GROUP BY`).

### Measure / Metric
A numeric quantity that can be aggregated across dimensions (e.g., `revenue`, `quantity`, `latency_ms`, `bytes_transferred`). Measures answer "how much" or "how many".

### Fact Table
A central table in an analytical schema containing numeric measures and foreign keys linking to dimension tables. Fact tables typically exhibit append-heavy write patterns and grow to millions or billions of rows.

### Dimension Table
A supporting table containing detailed attributes describing entities in a fact table (e.g., `dim_users`, `dim_products`). Dimension tables are typically wider, update less frequently, and contain fewer rows than fact tables.

### Star Schema
A database design pattern where a central fact table is directly connected to multiple radial dimension tables via foreign keys. It optimizes query simplicity, reduces join depth, and enables efficient star-join planning.

### Snowflake Schema
A variation of the star schema where dimension tables are normalized into further normalized sub-dimensions (e.g., `dim_products` joins to `dim_categories` which joins to `dim_departments`). While reducing redundancy, it increases join overhead in OLAP queries.

### Denormalization / Wide Table
The practice of pre-joining dimension attributes directly into the fact table, creating a single wide table (often 50–200+ columns). This eliminates query-time joins at the cost of storage redundancy—a tradeoff favored by columnar engines because unqueried columns cost nothing during scans.

---

## 2. Storage & Memory Layout

### Row-Oriented Storage (Heap)
A physical layout where all attributes of a single row are stored contiguously in memory and on disk (e.g., traditional PostgreSQL or MySQL 8KB pages). Excellent for point lookups and single-row transactions; disastrous for analytical aggregation across a subset of columns.

### Column-Oriented Storage (Columnar)
A physical layout where values for the same column across thousands or millions of rows are stored contiguously on disk and in memory (e.g., Parquet, ClickHouse MergeTree, DuckDB). Queries only read the columns explicitly requested, dramatically reducing disk I/O and maximizing compression.

### Row Group (Parquet)
A horizontal logical partitioning of data within a Parquet file, typically containing 100,000 to 1,000,000 rows. Within each row group, data is laid out column by column in column chunks.

### Column Chunk (Parquet)
The chunk of data for a specific column within a single row group. It contains one or more data pages and includes metadata (statistics, min/max values) for data skipping.

### Granule (ClickHouse)
The smallest, indivisible unit of data read from disk during a ClickHouse query. By default, a granule contains 8,192 rows. ClickHouse builds a sparse primary index containing one index mark per granule.

### Sparse Index
An index that contains one entry for a block of rows (e.g., one mark every 8,192 rows in ClickHouse) rather than an entry for every individual row (dense B-tree). It fits entirely in RAM and allows the engine to skip large swaths of disk blocks without row-level index lookups.

### Zone Map / Min-Max Statistics
Metadata stored alongside a block or row group recording the minimum and maximum value of each column in that block. If a query predicate is `WHERE created_at >= '2026-06-01'` and the block's `max(created_at) = '2026-05-31'`, the entire block is skipped without decompression.

### Bloom Filter Index
A probabilistic, memory-efficient data structure stored per block to test whether a given value might be present. It guarantees zero false negatives: if the Bloom filter reports an element is absent, the engine safely skips reading the block.

---

## 3. Compression & Encoding

### Dictionary Encoding
Replacing repeated string or high-overhead values with small compact integer IDs (e.g., 1-byte integers referencing a distinct dictionary array). Dramatically accelerates scans and grouping.

### Run-Length Encoding (RLE)
Representing consecutive identical values as a pair: `(value, count)`. Extremely effective on sorted columnar data (e.g., `(US, 50000)` instead of storing `US` 50,000 times).

### Delta Encoding
Storing the numerical difference between consecutive sorted values rather than the absolute values (e.g., timestamps `[100, 102, 105, 109]` become `[100, +2, +3, +4]`). When combined with bit-packing, integers require only 2–4 bits each.

### Bit Packing
Storing integers using only the exact number of bits required to represent the range of values in a block (e.g. storing numbers $0 \dots 7$ using 3 bits instead of 32 or 64 bits).

### Frame of Reference (FoR)
Subtracting the minimum value of a block from all values in that block, allowing large numbers to be represented as small offsets and tightly bit-packed.

---

## 4. Query Execution & Vectorization

### Volcano Iterator Model
The classic relational execution paradigm where operators implement a `next()` interface returning a single tuple at a time. High interpreter dispatch overhead and poor CPU cache utilization on large scans.

### Vectorized Execution (Block-at-a-Time)
An execution model where operators process arrays/vectors of values (e.g., 2048 values in DuckDB, 65536 values in ClickHouse) per function call. Amortizes interpreter dispatch overhead, fits working data in L1/L2 CPU caches, and allows compilers to generate SIMD instructions.

### SIMD (Single Instruction, Multiple Data)
CPU vector registers (e.g., AVX2, AVX-512, ARM Neon) capable of performing an operation (e.g., addition, comparison) on multiple data elements in a single clock cycle.

### Projection Pushdown
The query optimizer optimization of pushing column filtering down into the storage scanner, ensuring only columns referenced in the query are decompressed and loaded into memory.

### Predicate Pushdown
Evaluating filtering conditions directly at the storage layer (or during file scanning) using zone maps, dictionary IDs, or vector masks before materializing full rows.

### Partition Pruning
The static or dynamic elimination of entire physical partitions (directories or file sets) during query planning based on table partition keys and query predicates.

---

## 5. Aggregations & Joins

### Hash Aggregate
An aggregation algorithm where group keys are hashed into a hash table in memory to accumulate running aggregate states (count, sum). If distinct keys exceed available memory, partitions spill to disk.

### Distributive Aggregate
An aggregate function $f$ where the result for a combined set can be computed from the results of subsets: $f(A \cup B) = g(f(A), f(B))$ (e.g., `SUM`, `COUNT`, `MIN`, `MAX`). Essential for parallel and distributed aggregation.

### Algebraic Aggregate
An aggregate function expressible as a algebraic formula over distributive aggregates (e.g., `AVG` = `SUM` / `COUNT`).

### Holistic Aggregate
An aggregate function that cannot be computed by combining bounded-size partial states of subsets (e.g., `MEDIAN`, `PERCENTILE_CONT`, exact `COUNT(DISTINCT)`).

### HyperLogLog (HLL)
A probabilistic algorithm that estimates the number of distinct elements (cardinality) in a multiset using a fixed, small memory footprint (typically 1–12 KB) with a bounded error rate ($\approx 1\%$).

### t-Digest / DDSketch
Probabilistic data structures designed for accurate quantile and percentile estimation over continuous data streams with high precision at the tails (p99, p99.9).

### Hash Join
A join strategy where the engine builds an in-memory hash table on the join key of the smaller table (Build phase), and then streams vectors from the larger table to probe the hash table (Probe phase).

### Broadcast Join
In distributed query engines, sending a full copy of the smaller table to all worker nodes so each worker can join against its local partition of the large table without shuffling the large table.

### Partitioned / Shuffle Join
A distributed join strategy where both large tables are hashed and redistributed across the network by the join key so that rows with identical keys arrive at the same physical node.

---

## 6. Real-Time & Production Systems

### MergeTree (ClickHouse)
The core storage engine family of ClickHouse. Organizes data into immutable, sorted parts that are written during inserts and merged asynchronously in the background into larger parts.

### Segment (Druid / Pinot)
The immutable, columnar, time-partitioned unit of storage in Apache Druid and Apache Pinot. Typically contains 5M rows and includes column dictionaries, inverted bitmap indexes, and metric summaries.

### Ingestion Rollup
The aggregation of raw incoming events at ingestion time across a defined set of dimensions within a time bucket, permanently reducing raw storage requirements at the expense of granular detail.

### Materialized View
A database object containing the results of a query. In OLAP (such as ClickHouse), materialized views operate as continuous insertion triggers: newly inserted batches are transformed and appended into the target summary table without rescanning historical data.

### Projection (ClickHouse)
An alternative physical layout (different sorting key or pre-aggregated summary) of the same logical table stored alongside the primary parts, allowing queries to automatically select the optimal layout without query rewrite.

### Backpressure
The mechanism by which an analytical ingestion pipeline signals upstream producers (e.g. Kafka consumers) to pause or slow down when downstream storage or merge capacity is saturated.
