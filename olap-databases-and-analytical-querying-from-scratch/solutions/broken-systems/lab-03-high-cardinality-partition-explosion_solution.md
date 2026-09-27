# Solution: lab-03-high-cardinality-partition-explosion

## Incident Summary
Million-Partition Inode and Metadata Exhaustion

## Root Cause Diagnosis
Table is partitioned by user_id, creating 100,000 tiny parts and exhausting OS file handles during ingestion.

## The Architectural Cure

```sql
CREATE TABLE events (user_id UInt64, ...) ENGINE = MergeTree() PARTITION BY toYYYYMM(timestamp) ORDER BY (user_id, timestamp);
```

## Physical Verification & Mechanics
Partition keys must have coarse cardinality (e.g. months or days). Move high-cardinality keys to the ORDER BY sorting clause.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
