# Solution: EX-AGG-04

## Business Requirement
Error Rate and Total Requests per Microservice Endpoint

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    service_name,
    endpoint,
    COUNT(*) AS total_requests,
    COUNT(CASE WHEN http_status >= 500 THEN 1 END) AS errors,
    ROUND(COUNT(CASE WHEN http_status >= 500 THEN 1 END) * 100.0 / COUNT(*), 2) AS error_rate_pct
FROM service_logs
GROUP BY service_name, endpoint
ORDER BY error_rate_pct DESC, total_requests DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `service_name, endpoint, http_status` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
