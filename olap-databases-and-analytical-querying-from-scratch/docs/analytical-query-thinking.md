# The Analytical Query Thinking Framework

> "An analytical query is NOT complete merely because it returns the right answer. The engineer must understand every byte scanned, every block skipped, every vector passed through CPU cache, and how that query behaves when data volume increases 100-fold."

---

## The 18 Fundamental Invariant Questions

Whenever an analytical requirement, dashboard metric, or ad-hoc query is requested, you must answer these 18 mechanical questions **before** executing code or designing schemas:

```text
               ANALYTICAL REQUIREMENT
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
   LOGICAL INTENT                   PHYSICAL REALITY
┌──────────────────────┐         ┌──────────────────────┐
│ 1. Input Grain       │         │ 12. Partition Pruned?│
│ 2. Output Grain      │         │ 13. Block Skipped?   │
│ 3. Columns Needed    │         │ 14. Preaggregated?   │
│ 4. Temporal Range    │         │ 15. Bytes Scanned?   │
│ 5. Selectivity       │         │ 16. Aggregation RAM? │
│ 6. Aggregation?      │         │ 17. Network Shuffle? │
│ 7. Group Cardinality │         │ 18. Scale at 100x?   │
│ 8. Join Required?    │         └──────────────────────┘
│ 9. Table Sizes       │
│ 10. Sorting?         │
│ 11. Window Funcs?    │
└──────────────────────┘
```

---

### 1. What does one input row represent?
The **input grain** is the atomic contract of the source table.
- Does 1 row = one HTTP access log event?
- Does 1 row = an entire e-commerce shopping cart, or a single line item within that cart?
- Does 1 row = a point-in-time sensor reading, or a pre-aggregated 1-minute rollup?
*Mistake*: Joining or aggregating without knowing the grain leads to duplicate counts and inflated metrics.

### 2. What does one output row represent?
The **output grain** is the business contract of the final result set.
- Does 1 row = one tenant per calendar day?
- Does 1 row = a single user with their lifetime value and cohort label?
*Mistake*: Missing a grouping key or producing an unintended Cartesian product.

### 3. Which columns are required?
List **only** the physical column identifiers needed for projection, predicates, grouping keys, joins, and aggregations.
- In columnar storage, each referenced column incurs a separate disk and decompression cost.
- An unneeded column in `SELECT *` adds 100% unnecessary I/O.

### 4. Which rows / time range are required?
OLAP data is almost universally temporal. Identify the precise lower and upper boundaries (`WHERE event_time >= ? AND event_time < ?`).
- Are open-ended unbounded scans prevented?
- Is the predicate expressed on raw column values (enabling partition pruning) or wrapped in an opaque function (preventing pruning)?

### 5. What is the expected selectivity?
Selectivity is the ratio of rows passing the filter:
$$\text{Selectivity} = \frac{\text{Rows Matching Filter}}{\text{Total Rows in Table}}$$
- High selectivity (e.g., $0.0001\%$, 100 rows out of 100M): Ideal for sparse primary indexes, zone maps, or inverted indexes.
- Low selectivity (e.g., $85\%$, scanning almost everything): B-trees are useless. Sequential vectorized columnar scans will win by orders of magnitude.

### 6. Is aggregation required?
Is the query computing distributive aggregates (`SUM`, `COUNT`, `MIN`, `MAX`), algebraic aggregates (`AVG`), or holistic aggregates (`MEDIAN`, `PERCENTILE_CONT`, `COUNT(DISTINCT)`)?
- Distributive aggregates can be computed in parallel and merged across threads/nodes effortlessly.
- Holistic aggregates require either retaining all values or using approximation sketches (HyperLogLog, t-digest).

### 7. What is the grouping cardinality?
How many unique group keys exist in the result set?
- Low cardinality (e.g., `country` ~ 200 values, `status` ~ 5 values): Aggregation hash tables fit entirely within the CPU L2/L3 cache ($< 1 \text{ MB}$).
- Extreme cardinality (e.g., `user_id` ~ 50,000,000 values): Aggregation state requires gigabytes of RAM. If memory limit is breached, the engine must spill partitions to disk or crash with Out-Of-Memory (OOM).

### 8. Is a join required?
Can the query be answered from a single denormalized fact table, or must it join dimension or secondary fact tables?
- If joining: Which join algorithm will be chosen (Hash Join, Broadcast Join, Merge Join, or Colocated Partitioned Join)?

### 9. How large is each side of the join?
Compare the row count and byte volume of the Left side (Build/Probe) vs Right side:
- Small dimension ($< 100\text{ MB}$) $\times$ Giant fact ($500\text{ GB}$): Broadcast Join (replicate dimension into memory on each worker).
- Giant fact $\times$ Giant fact: Requires distributed hash partition shuffle across the network.

### 10. Is sorting required?
Does the query include `ORDER BY` with or without `LIMIT`?
- `ORDER BY col LIMIT 10`: Top-N heap optimization. Keeps only $K$ items in memory during scan ($O(N \log K)$).
- `ORDER BY col` without `LIMIT`: Requires sorting the full intermediate result set, often causing multi-way external merge sort on disk.

### 11. Is a window operation required?
Do you need running totals, lead/lag comparisons, or row numbering?
- Window functions require partitioning and sorting intermediate chunks. Does the partition key match the underlying storage distribution?

### 12. Can partitions be pruned?
Does the physical storage engine partition files by date or tenant?
- Will the engine skip entire directory trees or segment metadata without reading file footers?
- Verify via `EXPLAIN`: Ensure `Partitions Scanned` $\ll$ `Total Partitions`.

### 13. Can blocks or segments be skipped?
Do zone maps (min/max metadata per block/granule) or Bloom filters allow the query engine to skip reading compressed data pages?
- If the table is sorted by `(tenant_id, event_time)` and the query filters on `tenant_id = 42`, the engine should read $< 1\%$ of data granules.

### 14. Can the query use preaggregated data?
Does a Materialized View, Projection, or Ingestion Rollup already contain the grouped measures?
- Can we query a 1,000-row summary table instead of scanning a 1,000,000,000-row raw fact table?

### 15. How many bytes must be physically scanned?
Calculate the theoretical I/O requirement:
$$\text{Bytes Scanned} = \sum_{\text{cols}} (\text{Rows Passed Pruning} \times \text{Avg Compressed Col Width})$$
Compare this with the raw CSV / uncompressed size.

### 16. How much memory will aggregation require?
Estimate hash table memory:
$$\text{Memory} \approx \text{Distinct Keys} \times (\text{Key Size} + \text{State Size} + \text{Hash Overhead})$$
If estimated memory exceeds available engine `work_mem` / `max_memory_usage`, switch to approximate sketch or pre-aggregation.

### 17. Will execution require network shuffle?
In a distributed OLAP cluster (ClickHouse cluster, Druid, Pinot, Trino):
- Does data need to be repartitioned across nodes by group/join key?
- Network bandwidth is often $10\times$ slower than local memory bandwidth.

### 18. How will this query behave at 100× data?
If data volume scales from 10 million rows to 1 billion rows:
- Does the execution time scale linearly ($O(N)$), logarithmically ($O(\log N)$ via skipping), or catastrophically ($O(N^2)$ due to Cartesian join or nested loops)?
- Will it exceed RAM and trigger disk spilling?
- What physical design change must be planned today?
