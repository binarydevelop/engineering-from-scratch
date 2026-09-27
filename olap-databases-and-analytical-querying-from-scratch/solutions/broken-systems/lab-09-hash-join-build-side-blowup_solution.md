# Solution: lab-09-hash-join-build-side-blowup

## Incident Summary
Oversized Build Side in Distributed Hash Join

## Root Cause Diagnosis
Query planner puts a 50 GB fact table on the Build side and a 10 MB dimension table on the Probe side.

## The Architectural Cure

```sql
Ensure small table is on Build side or use Broadcast Join: /*+ BROADCAST(small_dim) */
```

## Physical Verification & Mechanics
Hash joins require loading the entire Build table into an in-memory hash table. Small table must always be the build relation.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
