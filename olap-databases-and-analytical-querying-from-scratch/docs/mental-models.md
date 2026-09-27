# OLAP Mental Models & Cognitive Maps

To design, query, and troubleshoot analytical databases efficiently, you must construct accurate mental models of what happens at the hardware and operating system levels.

---

## Mental Model 1: The Workload Invariant (OLTP vs OLAP)

```text
               OLTP                                    OLAP
──────────────────────────────────     ──────────────────────────────────
   "Many small needle-in-haystack"          "Fewer massive hay-baling passes"
               │                                       │
               ▼                                       ▼
       Point Key Lookup                         Full Table Scan
     (e.g., WHERE id = 10482)                (e.g., WHERE created_at >= '2026')
               │                                       │
               ▼                                       ▼
      Read Entire Single Row                 Read 2-3 Columns out of 60
 (All columns: name, addr, balance)      (Only: country, revenue across 100M rows)
               │                                       │
               ▼                                       ▼
       Frequent Row Updates                    Batch Append Only
    (ACID Transactions, Locks)               (Immutable Parts, Compactions)
               │                                       │
               ▼                                       ▼
      B-Tree Index Primary                    Sparse Index + Zone Maps + Sort Order
```

### The Core Contrast:
- **OLTP** assumes you want **all attributes of one row**. Storing rows together (row-store) minimizes disk head movement for point reads.
- **OLAP** assumes you want **one or two attributes across millions of rows**. Storing columns together (column-store) minimizes byte transfers by 90–98%.

---

## Mental Model 2: The Hardware Memory & Bandwidth Pyramid

When an analytical query runs across 100 million rows, memory latency and bandwidth determine performance:

```text
┌─────────────────────────────────────────┐  Latency     Bandwidth
│ L1 Cache: ~64 KB per core              │  ~1.0 ns     ~2,000 GB/s
│ └─ Vectorized inner loops run here     │
├─────────────────────────────────────────┤
│ L2 Cache: ~1-2 MB per core             │  ~3.5 ns     ~1,000 GB/s
│ └─ Hash table buckets for group keys   │
├─────────────────────────────────────────┤
│ L3 Shared Cache: ~32-128 MB            │  ~12.0 ns    ~400 GB/s
│ └─ In-flight data chunks (DuckDB/CH)   │
├─────────────────────────────────────────┤
│ System RAM (DDR5 / Unified): 32-256 GB │  ~60.0 ns    ~50-100 GB/s
│ └─ Working memory for large joins/sorts│
├─────────────────────────────────────────┤
│ NVMe PCIe Gen4 SSD: 1-8 TB             │  ~15-50 µs   ~3-7 GB/s
│ └─ Sequential compressed column scans  │
├─────────────────────────────────────────┤
│ Network / S3 Object Store: Unlimited   │  ~20-100 ms  ~0.1-1.25 GB/s (10GbE)
│ └─ Distributed shuffle / lakehouse     │
└─────────────────────────────────────────┘
```

### The Architectural Consequence:
1. **Row Store Failure**: In a row store, reading 100M rows to sum 1 column requires streaming all unused columns across the slow NVMe and RAM buses into CPU cache. The CPU stalls on memory bandwidth.
2. **Column Store Superpower**: In a column store, only the target column is read sequentially from NVMe. Values of identical types compress tightly (e.g., LZ4, Delta, RLE). When loaded into CPU registers, SIMD instructions process 4–16 values per CPU clock cycle.

---

## Mental Model 3: The Complete Query Execution Path

```text
                           Raw SQL Query
                                │
                                ▼
                       [1. SQL Parser]
                       (Produces AST)
                                │
                                ▼
                   [2. Logical Plan Builder]
         (LogicalScan -> Filter -> Aggregate -> Sort)
                                │
                                ▼
                     [3. Query Optimizer]
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
  [Rule-Based Optimizations]                 [Cost-Based Estimation]
  - Filter Pushdown                          - Cardinality Estimation
  - Projection Pushdown                      - Join Order Selection
  - Constant Folding                         - Hash vs Broadcast Join
         │                                             │
         └──────────────────────┬──────────────────────┘
                                │
                                ▼
                   [4. Physical Plan Builder]
          (VectorScan -> FilterVector -> HashAggregate)
                                │
                                ▼
                 [5. Physical Storage Engine]
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
[Partition Pruning]      [Zone Map Skipping]   [Sparse Mark Index]
(Eliminates file paths)  (Skips blocks/chunks) (Skips granules)
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                                │
                                ▼
              [6. Column Decompression & Decoding]
               (Dictionary, RLE, BitUnpack, LZ4)
                                │
                                ▼
             [7. Vectorized Execution Pipeline]
            (Streams 2048-row chunks in L2/L3 cache)
                                │
                                ▼
             [8. Partial Aggregate Accumulation]
              (Local hash table per CPU worker)
                                │
                                ▼
             [9. Global Merge / Final Projection]
            (Combines worker states into final rows)
```

---

## Mental Model 4: Distributed OLAP Communication (Shuffle vs Broadcast)

```text
Case A: Broadcast Join (Large Fact Table ⨝ Small Dimension Table)
┌──────────────┐     ┌──────────────┐
│ Worker Node 1│     │ Worker Node 2│
│  [Fact Part] │     │  [Fact Part] │
│      ⨝       │     │      ⨝       │
│  [Full Dim]  │     │  [Full Dim]  │
└──────▲───────┘     └──────▲───────┘
       │                    │
       └─────────┬──────────┘
                 │ (Broadcast Small Dim once: 5 MB)
          [Coordinator]

Case B: Partitioned / Shuffle Join (Large Fact Table ⨝ Large Fact Table)
┌──────────────┐                    ┌──────────────┐
│ Worker Node 1│ ──(Hash Key % 2)──>│ Worker Node 2│
│  [Fact A1]   │ <──(Hash Key % 2)──│  [Fact A2]   │
│  [Fact B1]   │                    │  [Fact B2]   │
└──────────────┘                    └──────────────┘
       ▲                                   ▲
       └─────────────────┬─────────────────┘
                         │
                 Heavy Network I/O!
        (Both giant tables shuffled across wires)
```
