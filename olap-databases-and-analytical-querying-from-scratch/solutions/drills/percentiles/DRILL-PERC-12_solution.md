# Solution: DRILL-PERC-12

## Drill
Latency Percentile & SLA Drill #12

## Solution SQL

```sql
SELECT
    endpoint,
    approx_quantile(latency_ms, 0.95)
FROM service_logs
GROUP BY endpoint
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `endpoint` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
