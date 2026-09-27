# Solution: lab-01-select-star-io-explosion

## Incident Summary
SELECT * Columnar I/O Explosion

## Root Cause Diagnosis
A dashboard query issues SELECT * against a 60-column fact table across 10 million rows, causing severe NVMe I/O saturation and 8-second query latency.

## The Architectural Cure

```sql
SELECT country, SUM(net_revenue) FROM fact_order_items WHERE created_at >= '2025-01-01' GROUP BY country;
```

## Physical Verification & Mechanics
Columnar storage allows reading only referenced column files. SELECT * forces opening and decompressing all 60 columns. Projecting only 2 columns reduces I/O by 95%.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
