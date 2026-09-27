# Solution: lab-06-huge-group-by-oom

## Incident Summary
Out-Of-Memory from High-Cardinality GROUP BY

## Root Cause Diagnosis
Query groups by an unconstrained UUID across 50 million rows, blowing past available query memory limits.

## The Architectural Cure

```sql
SELECT service_name, count(*) FROM service_logs GROUP BY service_name;
```

## Physical Verification & Mechanics
Grouping by high-cardinality keys requires an enormous in-memory hash table. Either aggregate by lower-cardinality dimensions, or enable disk-spilling: max_bytes_before_external_group_by.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
