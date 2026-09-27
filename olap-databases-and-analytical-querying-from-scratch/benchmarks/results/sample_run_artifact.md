# Benchmark: Row (CSV) vs Columnar (Parquet) Scan & Aggregation

## 1. Question
How does row-oriented vs columnar storage impact query latency and byte traversal when aggregating 2 columns out of 14 across 50,000 order items?

## 2. Hypothesis
Columnar Parquet storage will scan < 15% of raw bytes and execute 10x-50x faster than CSV due to column projection pushdown and avoiding string row deserialization.

## 3. Database / Version
- **Database Engine**: DuckDB
- **Version**: 1.5.5
- **Deployment Mode**: Local in-process

## 4. Hardware Environment
- **CPU**: Apple Silicon M-series (ARM64)
- **RAM**: 16 GB Unified Memory (DuckDB thread limit: 4, memory limit: 4GB)
- **Storage**: Apple NVMe SSD (Sequential Read ~3,000 MB/s)
- **Operating System**: macOS Darwin 24.x

## 5. Dataset Specifications
- **Domain**: `ecommerce` (fact_order_items)
- **Rows**: 50,000 rows
- **Columns**: 14 columns
- **Uncompressed CSV Size**: 2.7 MB
- **Compressed Parquet Size**: 668 KB
- **Compression Ratio**: 4.04:1 (ZSTD)

## 6. Query
```sql
SELECT country, COUNT(*) as cnt, SUM(net_revenue) as rev
FROM read_parquet('datasets/ecommerce/fact_order_items.parquet')
GROUP BY country
ORDER BY rev DESC;
```

## 7. Execution Parameters
- **Cache State**: Cold & Warm measured
- **Warmup Runs**: 2
- **Measured Runs**: 5
- **Concurrency**: 1

## 8. Latency Metrics

| Format / Storage | p50 (ms) | Mean (ms) | p95 (ms) | Rows Out | Speedup vs CSV |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CSV (Row Scan)** | 62.56 ms | 62.98 ms | 65.98 ms | 6 | 1.00x (Baseline) |
| **Parquet (Columnar Pushdown)** | 1.02 ms | 1.02 ms | 1.07 ms | 6 | **61.28x faster** |
| **DuckDB Native Table** | 1.65 ms | 1.69 ms | 1.77 ms | 6 | **37.92x faster** |

## 9. Physical Resource Utilization
- **Rows Read**: 50,000 rows
- **Columns Loaded**: 2 out of 14 (85.7% columns skipped)
- **Bytes Scanned**: ~160 KB (Parquet) vs 2,700 KB (CSV)
- **Peak Memory**: < 2 MB

## 10. Architectural Interpretation
1. **Projection Pushdown**: In Parquet, DuckDB only requested the byte ranges for the `country` and `net_revenue` column chunks. The remaining 12 columns were never loaded from storage.
2. **Deserialization Avoidance**: CSV parsing required ASCII-to-integer, ASCII-to-timestamp, and ASCII-to-float conversions for all 14 columns. Parquet stored values directly in binary Little-Endian format ready for SIMD registers.

## 11. Limitations & Boundary Conditions
If a query requested `SELECT * FROM table`, Parquet would have to open and decompress all 14 column chunks, narrowing the performance gap. Furthermore, for single-row point lookups (`WHERE order_item_id = 42`), a row-oriented B-tree index in PostgreSQL would execute in < 0.1 ms without scanning files.
