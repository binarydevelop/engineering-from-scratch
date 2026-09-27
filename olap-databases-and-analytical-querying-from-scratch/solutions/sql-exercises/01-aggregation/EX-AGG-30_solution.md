# Solution: EX-AGG-30

## Business Requirement
Multi-Measure Aggregation and Group Filter Drill #30

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    category AS group_dim,
    COUNT(*) AS event_count,
    ROUND(SUM(net_revenue), 2) AS total_metric,
    ROUND(AVG(net_revenue), 2) AS avg_metric
FROM fact_order_items
GROUP BY category
HAVING COUNT(*) > 300
ORDER BY total_metric DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `created_at, category, net_revenue` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> Filter -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
