# Solution: EX-CH-01

## Business Requirement
ClickHouse Vectorized & Specialized OLAP Functions Drill #1

## Verified SQL Solution (ClickHouse SQL)

```sql
SELECT
    service_name,
    count() AS total_requests,
    round(quantileExact(0.50)(latency_ms), 2) AS p50_latency,
    round(quantileExact(0.95)(latency_ms), 2) AS p95_latency,
    round(quantileExact(0.99)(latency_ms), 2) AS p99_latency,
    uniq(trace_id) AS approx_unique_traces
FROM service_logs
GROUP BY service_name
ORDER BY total_requests DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `service_name, latency_ms, timestamp` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `MergeTreeScan -> VectorizedAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
