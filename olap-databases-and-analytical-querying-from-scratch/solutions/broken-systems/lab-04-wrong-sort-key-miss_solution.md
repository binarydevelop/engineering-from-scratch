# Solution: lab-04-wrong-sort-key-miss

## Incident Summary
Sort Key Miss Leading to 100% Block Scan

## Root Cause Diagnosis
Table is sorted by (event_id), but 99% of queries filter by (tenant_id, timestamp), rendering sparse primary indexes and zone maps ineffective.

## The Architectural Cure

```sql
Reorder table primary sorting key: ORDER BY (tenant_id, timestamp, event_id);
```

## Physical Verification & Mechanics
ClickHouse and Parquet zone maps can only skip blocks if the filter column appears early in the sorted key hierarchy.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
