# Benchmark Specification and Reporting Template

Every performance claim in this repository must be backed by a completed instance of this benchmark report. Unsubstantiated performance claims ("Database X is 100x faster than Database Y") are strictly prohibited.

---

## 1. Question
What specific architectural or algorithmic question is this benchmark measuring?
*(e.g., How does row-oriented vs columnar storage impact query latency when aggregating 3 columns out of 50 across 10 million rows?)*

---

## 2. Hypothesis
State your mechanical prediction before running the benchmark:
*(e.g., Columnar storage will scan < 10% of raw bytes and execute 8–15× faster due to SIMD vectorization and avoiding unreferenced attribute deserialization.)*

---

## 3. Database / Version
- **Database Engine**: DuckDB / ClickHouse / PostgreSQL / Apache Druid
- **Exact Version**: (e.g., DuckDB 1.5.5, ClickHouse 24.8.4, PostgreSQL 16.4)
- **Deployment Mode**: Local embedded in-process / Docker single-node container / Multi-node cluster

---

## 4. Hardware Environment
- **CPU**: (e.g., Apple M-series ARM64 / Intel Xeon / AMD EPYC, number of physical & logical cores)
- **RAM**: Total system memory and configured engine limits (e.g., 16 GB unified RAM, DuckDB memory_limit=4GB)
- **Storage**: (e.g., Apple NVMe SSD, sequential read bandwidth ~3,000 MB/s, IOPS)
- **Operating System**: macOS 15.x / Linux Ubuntu 22.04 LTS kernel version

---

## 5. Dataset Specifications
- **Dataset Domain**: `ecommerce` / `clickstream` / `observability` / `ads` / `finance` / `iot`
- **Total Row Count**: (e.g., 10,000,000 rows)
- **Total Columns**: (e.g., 32 columns with mixed types: int64, float64, string, timestamp, uuid)
- **Data Distribution**: Uniform / Zipfian skew (alpha=1.2) / Monotonic temporal
- **Uncompressed Size**: (e.g., 4.8 GB in raw uncompressed CSV)
- **Compressed Size**: (e.g., 480 MB in Parquet with Snappy/ZSTD or ClickHouse MergeTree with LZ4)
- **Compression Ratio**: (e.g., 10:1)

---

## 6. Query Specification
Provide the exact SQL query executed during the benchmark:

```sql
SELECT
    country,
    COUNT(*) AS total_events,
    SUM(revenue) AS total_revenue,
    AVG(duration_ms) AS avg_duration
FROM events_table
WHERE event_timestamp >= '2026-01-01' AND event_timestamp < '2026-02-01'
GROUP BY country
ORDER BY total_revenue DESC;
```

---

## 7. Execution Parameters
- **Cache State**: Cold (OS page cache dropped or direct I/O) vs Warm (cache primed)
- **Warmup Iterations**: (e.g., 3 runs discarded)
- **Measured Iterations**: (e.g., 10 runs recorded)
- **Concurrency**: (e.g., 1 client thread vs 16 concurrent workers)

---

## 8. Latency Metrics

| Metric | Measured Value (ms) |
| :--- | :--- |
| **p50 (Median)** | |
| **p95** | |
| **p99** | |
| **Min** | |
| **Max** | |
| **Mean ± StdDev** | |

---

## 9. Physical Resource Utilization

| Metric | Measured Quantity |
| :--- | :--- |
| **Rows Read / Considered** | |
| **Rows Returned** | |
| **Bytes Physically Scanned** | |
| **Peak Memory (RAM)** | |
| **User CPU Time** | |
| **System CPU Time** | |
| **Storage Read Bandwidth** | |

---

## 10. Query Plan & Operator Profile
Attach the output of `EXPLAIN ANALYZE` or database execution profile:

```text
-- Physical Execution Tree
```

---

## 11. Architectural Interpretation
Explain the physical mechanisms that account for the observed metrics:
- Why did one engine or layout outperform another?
- Was the execution memory-bound, I/O-bound, or compute-bound?
- Did vectorization, dictionary encoding, or partition pruning account for the differential?

---

## 12. Limitations & Boundary Conditions
Document all caveats:
- What biases exist in the synthetic data distribution?
- Under what inverted access pattern (e.g., single-row point updates) would this winning architecture severely degrade?
- Why does this result NOT prove a universal "fastest database" claim?
