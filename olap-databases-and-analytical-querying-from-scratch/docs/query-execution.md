# Modern OLAP Query Execution: Vectorization & Pipelines

How does an analytical database execute a SQL query across 100 million rows in 50 milliseconds? This document explores query execution from CPU instruction dispatch to vectorized pipelining.

---

## 1. The Death of the Volcano Iterator Model

Traditional relational databases (PostgreSQL, SQLite, Oracle 7) execute queries using the **Volcano iterator model** (also known as the Tuple-at-a-Time model):

```cpp
// Traditional Volcano Iterator
class Operator {
    virtual Tuple* next() = 0;
};
```

When evaluating `SELECT revenue * 1.08 FROM orders WHERE country = 'US';`:
1. The `Filter` operator calls `Scan->next()` to retrieve a single row tuple.
2. It executes a virtual function call to check `country == 'US'`.
3. If true, the `Project` operator calls `Filter->next()` and computes `revenue * 1.08`.
4. This entire virtual method dispatch loop repeats for **every single row**.

### The Three Fatal Bottlenecks on Modern CPUs:
1. **Virtual Function Dispatch Overhead**: For 100M rows, calling `next()` requires 100M indirect function calls. Modern CPU branch predictors are thrashed by polymorphic method pointers.
2. **CPU Instruction Cache (I-Cache) Thrashing**: The CPU instruction pointer continuously jumps between `Scan::next`, `Filter::next`, and `Project::next`.
3. **Memory Latency & Poor Cache Locality**: Reading a tuple containing 30 columns into cache registers just to check one column wastes 95% of L1/L2 cache capacity.

---

## 2. Vectorized Execution (Block-at-a-Time)

Pioneered by MonetDB/X100 (now VectorWise) and adopted by **DuckDB** and **ClickHouse**, vectorized execution replaces single-tuple dispatch with contiguous array vectors:

```cpp
// Vectorized Operator Interface
class VectorizedOperator {
    virtual void process(DataChunk &input, DataChunk &output) = 0;
};
```

Instead of passing 1 tuple, the engine passes a **DataChunk** containing a fixed batch of rows (e.g., 2,048 rows in DuckDB, 65,536 rows in ClickHouse):

```text
DataChunk (2,048 rows):
  Vector 1 [country]:  ["US", "DE", "US", "FR", ...]
  Vector 2 [revenue]:  [120.5, 45.0, 89.2, 310.0, ...]
```

### Why Vectorization is 10× to 50× Faster:
1. **Amortized Function Calls**: Evaluating 2,048 rows requires only **one** virtual function call, reducing dispatch overhead by $99.95\%$.
2. **Trivial Inner Loops**: The filtering loop becomes a tight, contiguous C/C++ array loop:
   ```cpp
   for (size_t i = 0; i < 2048; ++i) {
       mask[i] = (country[i] == US_CODE);
   }
   ```
3. **SIMD Auto-Vectorization**: Modern compilers (Clang/GCC) automatically transform this loop into SIMD vector instructions (AVX2, AVX-512, ARM Neon). A single CPU clock cycle compares 8 or 16 values simultaneously!
4. **Zero Branch Mispredictions**: Branchless selection masks eliminate CPU pipeline stalls.

---

## 3. Push-Based Pipeline Execution

Traditional pull-based systems pull data from bottom to top (`Consumer -> next() -> Producer`). Modern OLAP engines (DuckDB, ClickHouse, HyPer) use **Push-Based Pipelines**:

```text
[Table Scan Source]
        │  (Pushes DataChunk of 2048 rows)
        ▼
   [Filter Operator]  ──(Applies vector mask in L1 cache)
        │  (Pushes filtered chunk)
        ▼
  [Hash Aggregate]   ──(Accumulates into thread-local hash table)
        │
        ▼  (When scan completes, pushes state)
 [Global Aggregation Sink]
```

### The In-Cache Advantage:
A DataChunk (2,048 values $\times$ 8 bytes = 16 KB) fits entirely inside the core's private **L1 Data Cache (32–64 KB)**. The chunk is scanned, filtered, transformed, and aggregated **while remaining in the CPU cache**, without ever being evicted back to slower RAM!

---

## 4. Hash Aggregation Algorithms

When executing `GROUP BY category, country`:
1. **Low Cardinality (Perfect Hash Table)**:
   If the grouping dimensions have small integer ranges (e.g. `category_id < 100`), the engine uses a direct flat array lookup with zero hash collisions.
2. **Medium Cardinality (Thread-Local Hash Table)**:
   Each CPU core maintains its own linear-probing hash table. No thread locks or atomic memory barriers are needed during the scan phase.
3. **Global Merge Phase**:
   When all worker threads finish scanning their assigned data blocks, their local hash tables are combined into a final result table.
4. **High Cardinality Spill**:
   If the hash table exceeds configured memory (`max_memory_usage` or `max_memory`), the engine partitions data by the hash prefix and spills excess partitions to disk.
