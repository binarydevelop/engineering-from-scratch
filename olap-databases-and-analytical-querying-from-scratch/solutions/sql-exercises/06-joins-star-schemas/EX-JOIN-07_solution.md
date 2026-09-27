# Solution: EX-JOIN-07

## Business Requirement
Star Schema Multi-Way Dimension Join Drill #7

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    u.user_segment,
    p.brand,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(f.net_revenue), 2) AS gross_revenue,
    ROUND(AVG(f.price - p.cost), 2) AS avg_margin
FROM fact_order_items f
JOIN dim_users u ON f.user_id = u.user_id
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY u.user_segment, p.brand
ORDER BY gross_revenue DESC
LIMIT 50;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `user_id, product_id, net_revenue, user_segment, brand` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashJoin(dim_users) -> HashJoin(dim_products) -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `5` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
