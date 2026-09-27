# Solution: lab-02-unpartitioned-date-scan

## Incident Summary
Full Table Scan from Unpruned Date Predicate

## Root Cause Diagnosis
Query filters by wrapping a column in a function (e.g. toYear(created_at) = 2025), preventing partition pruning and forcing a full scan of 5 years of historical data.

## The Architectural Cure

```sql
SELECT count(*) FROM fact_order_items WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
```

## Physical Verification & Mechanics
Non-sargable expressions prevent the query planner from matching partition boundaries. Using direct constant range comparisons prunes 80% of partitions.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
