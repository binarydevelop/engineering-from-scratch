# Solution: EX-WIN-04

## Business Requirement
Analytical Window Function Drill #4: Running Totals and Trailing Lags

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    user_id,
    created_at AS event_time,
    net_revenue AS current_value,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS seq_num,
    LAG(net_revenue) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_value,
    ROUND(SUM(net_revenue) OVER (PARTITION BY user_id ORDER BY created_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_total
FROM fact_order_items
ORDER BY user_id, event_time
LIMIT 100;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `user_id, created_at, net_revenue` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> Sort -> WindowOperator`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
