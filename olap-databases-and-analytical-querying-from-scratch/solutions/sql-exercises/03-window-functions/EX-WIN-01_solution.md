# Solution: EX-WIN-01

## Business Requirement
Analytical Window Function Drill #1: Running Totals and Trailing Lags

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    user_id,
    event_time AS event_time,
    duration_ms AS current_value,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time) AS seq_num,
    LAG(duration_ms) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_value,
    ROUND(SUM(duration_ms) OVER (PARTITION BY user_id ORDER BY event_time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_total
FROM web_events
ORDER BY user_id, event_time
LIMIT 100;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `user_id, event_time, duration_ms` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> Sort -> WindowOperator`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
