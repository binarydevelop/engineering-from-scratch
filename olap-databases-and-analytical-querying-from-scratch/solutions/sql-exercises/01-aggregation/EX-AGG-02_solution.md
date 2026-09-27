# Solution: EX-AGG-02

## Business Requirement
Category Average Price, Min and Max Order Value

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    category,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(MIN(price), 2) AS min_price,
    ROUND(MAX(price), 2) AS max_price
FROM fact_order_items
GROUP BY category
ORDER BY avg_price DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `category, price` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `2` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
