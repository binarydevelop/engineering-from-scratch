# Analytical Query Specification Template

Every analytical query exercise in this curriculum must adhere to this contract. A query is **not** complete merely because it produces rows; it must be fully characterized across logical requirements and physical execution.

---

## Exercise Metadata

- **Exercise ID**: `EX-[CATEGORY]-[NUMBER]`
- **Dataset**: `ecommerce` | `clickstream` | `observability` | `ads` | `finance` | `iot`
- **Difficulty**: `Foundational` | `Intermediate` | `Advanced` | `Expert Mastery`
- **SQL Dialect**: `ANSI SQL` | `DuckDB` | `ClickHouse SQL` | `PostgreSQL` | `Druid SQL`

---

## 1. Requirement & Business Question
State the exact analytical question asked by leadership, product, or engineering operations.
*Example: Compute the 7-day trailing average revenue per active user grouped by acquisition cohort and traffic channel.*

---

## 2. Relational Grains

- **Input Grain**:
  *What does exactly ONE row in the primary source table represent?*
  *(e.g., One HTTP access log event emitted by nginx)*

- **Expected Output Grain**:
  *What does exactly ONE row in the final result set represent?*
  *(e.g., One country + calendar month pair)*

- **Expected Row Count / Result Shape**:
  *(e.g., ~180 rows, 4 columns: [country, month, active_users, trailing_avg_rev])*

---

## 3. Physical Execution Predictions

Before executing, predict the exact physical resources required:

- **Expected Columns Scanned**:
  *(List strictly the columns necessary to satisfy projection, filtering, grouping, and joining)*

- **Expected Major Physical Operators**:
  *(e.g., TableScan -> Filter -> HashAggregate -> WindowOperator -> TopN/Sort)*

- **Expected Partition Pruning**:
  *(Can the engine skip file partitions or parts based on predicate constants? Yes/No, explain)*

- **Data Skipping Potential**:
  *(Can zone maps, Bloom filters, or sparse primary indexes eliminate data blocks?)*

- **Performance Sensitivity**:
  *(e.g., High-cardinality grouping hazard, wide string shuffle risk, window frame memory pressure)*

---

## 4. Query Implementation

```sql
-- Solution SQL Query
SELECT
    -- Dimensions & Measures
FROM
    -- Sources & Joins
WHERE
    -- Selective Predicates
GROUP BY
    -- Aggregation Keys
ORDER BY
    -- Ordering
;
```

---

## 5. Physical Plan Verification

Inspect the query plan using `EXPLAIN ANALYZE` or database profiler:

```text
-- Physical Plan Output Paste
```

- **Actual Rows Scanned vs Returned**:
- **Actual Bytes Read**:
- **Filter Pushdown Verified**: [Yes / No]
- **Projection Pushdown Verified**: [Yes / No]

---

## 6. Advanced Physical Reasoning (For Intermediate & Advanced)

- **Which part of this query is the most expensive physical bottleneck?**
  *(e.g., Hash table probe during join, memory spill during window partition sort, or string decompression during scan)*

- **How would you prove this bottleneck using execution metrics?**
  *(e.g., Profiling CPU instructions vs I/O wait, comparing L3 cache misses, checking clickhouse query_log memory metrics)*

- **What physical schema or storage layout change would accelerate this by 10×?**
  *(e.g., Reordering the MergeTree sort key by tenant_id, dictionary-encoding low-cardinality strings, or building an incremental projection)*
