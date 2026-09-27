# Solution: EX-AGG-01

## Business Requirement
Total Revenue and Orders by Country

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    country,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_revenue), 2) AS total_revenue
FROM fact_order_items
GROUP BY country
ORDER BY total_revenue DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `country, order_id, net_revenue` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate -> TopNSort`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
