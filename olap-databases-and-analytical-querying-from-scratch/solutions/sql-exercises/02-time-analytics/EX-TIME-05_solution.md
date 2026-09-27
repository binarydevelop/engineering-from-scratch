# Solution: EX-TIME-05

## Business Requirement
Temporal Resampling and Metrics by Month Drill #5

## Verified SQL Solution (DuckDB)

```sql
SELECT
    date_trunc('month', timestamp) AS time_bucket,
    COUNT(*) AS total_records,
    ROUND(AVG(temperature_c), 2) AS avg_value,
    ROUND(SUM(temperature_c), 2) AS total_value
FROM sensor_readings
WHERE timestamp >= '2025-01-01'
GROUP BY 1
ORDER BY time_bucket ASC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `timestamp, temperature_c` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> Filter -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `2` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
