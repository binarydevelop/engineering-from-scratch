# Solution: DRILL-DATE-14

## Drill
Date Truncation & Gap Fill Drill #14

## Solution SQL

```sql
SELECT
    date_trunc('hour', timestamp),
    COUNT(*), AVG(latency_ms)
FROM service_logs
GROUP BY date_trunc('hour', timestamp)
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `date_trunc('hour', timestamp)` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
