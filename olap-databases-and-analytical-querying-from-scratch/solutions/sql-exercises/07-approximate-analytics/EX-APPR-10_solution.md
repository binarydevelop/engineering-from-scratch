# Solution: EX-APPR-10

## Business Requirement
Approximate Distinct Counting & Sketches Drill #10

## Verified SQL Solution (DuckDB)

```sql
SELECT
    page_url,
    approx_count_distinct(user_id) AS approx_unique_users,
    COUNT(DISTINCT user_id) AS exact_unique_users,
    COUNT(*) AS total_hits
FROM web_events
GROUP BY page_url
ORDER BY total_hits DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `page_url, user_id` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> ApproxCountDistinct (HyperLogLog)`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `2` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
