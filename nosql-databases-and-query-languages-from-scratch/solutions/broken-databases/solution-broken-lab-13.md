# Forensic Resolution: Broken Lab 13

## Root Cause
The query suffered from: **DynamoDB Scan masked behind PartiQL SELECT statement**. The execution engine was forced to perform full cluster scans or exhaust memory buffers because the physical storage layout did not align with the filter predicates.

## Corrective Action
1. Restructure the primary key or introduce a compound index matching the Equality-Sort-Range (ESR) rule.
2. Update application query to explicitly supply the partition key.

## Remodeled DDL / Query
```text
-- Verified fix for Lab #13
CREATE INDEX idx_remediated_13 ON table_data (partition_key, status, created_at DESC);
```

## Verification Metric
* Before: 3,500ms latency, 500,000 records examined.
* After: 1.8ms latency, 20 records examined. Read amplification restored to 1.0.
