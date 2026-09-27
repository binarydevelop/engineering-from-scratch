# Solution: EX-TIME-16

## Business Requirement
Temporal Resampling and Metrics by Hour Drill #16

## Verified SQL Solution (DuckDB)

```sql
SELECT
    date_trunc('hour', created_at) AS time_bucket,
    COUNT(*) AS total_records,
    ROUND(AVG(net_revenue), 2) AS avg_value,
    ROUND(SUM(net_revenue), 2) AS total_value
FROM fact_order_items
WHERE created_at >= '2025-01-01'
GROUP BY 1
ORDER BY time_bucket ASC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `created_at, net_revenue` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> Filter -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `2` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
