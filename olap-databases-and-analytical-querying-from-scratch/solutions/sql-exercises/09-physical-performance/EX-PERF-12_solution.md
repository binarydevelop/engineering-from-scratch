# Solution: EX-PERF-12

## Business Requirement
Physical Execution & Plan Optimization Challenge #12

## Verified SQL Solution (DuckDB)

```sql
EXPLAIN ANALYZE
SELECT
    country,
    category,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    COUNT(*) AS item_count
FROM fact_order_items
WHERE created_at >= '2025-01-01' AND created_at < '2025-06-01'
GROUP BY country, category
ORDER BY total_revenue DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `country, category, net_revenue` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan (with Projection Pushdown) -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
