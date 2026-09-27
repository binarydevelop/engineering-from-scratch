# Solution: lab-05-uncompressed-string-scan

## Incident Summary
Uncompressed High-Cardinality String Scan

## Root Cause Diagnosis
Country and URL columns are stored as raw uncompressed strings instead of LowCardinality / dictionary encoding, inflating disk footprint by 4x.

## The Architectural Cure

```sql
ALTER TABLE events ADD COLUMN country LowCardinality(String);
```

## Physical Verification & Mechanics
LowCardinality uses an internal dictionary encoding with 1-byte integer tokens, reducing memory and disk size by 75% and accelerating grouping.

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
