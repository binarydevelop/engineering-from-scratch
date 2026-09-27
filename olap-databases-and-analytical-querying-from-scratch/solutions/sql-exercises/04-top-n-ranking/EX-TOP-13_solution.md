# Solution: EX-TOP-13

## Business Requirement
Top-N Products by Revenue within Each Region Drill #13

## Verified SQL Solution (ANSI SQL)

```sql
WITH ranked_products AS (
    SELECT
        country,
        product_id,
        ROUND(SUM(net_revenue), 2) AS total_revenue,
        DENSE_RANK() OVER (PARTITION BY country ORDER BY SUM(net_revenue) DESC) AS rank_pos
    FROM fact_order_items
    GROUP BY country, product_id
)
SELECT country, product_id, total_revenue, rank_pos
FROM ranked_products
WHERE rank_pos <= 6
ORDER BY country, rank_pos;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `country, product_id, net_revenue` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate -> WindowSort -> Filter`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
