# Solution: EX-AGG-15

## Business Requirement
Multi-Measure Aggregation and Group Filter Drill #15

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    service_name AS group_dim,
    COUNT(*) AS event_count,
    ROUND(SUM(latency_ms), 2) AS total_metric,
    ROUND(AVG(latency_ms), 2) AS avg_metric
FROM service_logs
GROUP BY service_name
HAVING COUNT(*) > 150
ORDER BY total_metric DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `created_at, service_name, latency_ms` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> Filter -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
