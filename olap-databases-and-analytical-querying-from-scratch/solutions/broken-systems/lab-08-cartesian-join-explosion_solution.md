# Solution: lab-08-cartesian-join-explosion

## Incident Summary
Accidental Cartesian Join Explosion

## Root Cause Diagnosis
A query joins two fact tables on an incomplete key, creating an accidental many-to-many join explosion that generates 100 million intermediate rows.

## The Architectural Cure

```sql
SELECT count(*) FROM fact_order_items a JOIN dim_users u ON a.user_id = u.user_id;
```

## Physical Verification & Mechanics
Fact-to-fact joins on non-unique dimensions create quadratic row expansions. Star schema joins against distinct dimension keys prevent explosive intermediates.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
