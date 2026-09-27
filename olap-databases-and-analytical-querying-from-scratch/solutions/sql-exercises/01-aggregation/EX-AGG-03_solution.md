# Solution: EX-AGG-03

## Business Requirement
Event Count and Average Duration by Browser and Device OS

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    browser,
    device_os,
    COUNT(*) AS total_events,
    ROUND(AVG(duration_ms), 1) AS avg_duration_ms
FROM web_events
GROUP BY browser, device_os
ORDER BY total_events DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `browser, device_os, duration_ms` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
