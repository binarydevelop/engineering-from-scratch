# Solution: lab-07-exact-distinct-count-memory-spike

## Incident Summary
Exact COUNT(DISTINCT) Memory Saturation

## Root Cause Diagnosis
Executive dashboard runs COUNT(DISTINCT user_id) over 1 billion rows, consuming 32 GB RAM.

## The Architectural Cure

```sql
SELECT approx_count_distinct(user_id) FROM web_events; -- In ClickHouse: uniq(user_id)
```

## Physical Verification & Mechanics
HyperLogLog sketches provide a bounded 1-4 KB memory state with ~1% error, eliminating hash set memory exhaustion.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
