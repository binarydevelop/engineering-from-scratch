# Solution: DRILL-OPTI-05

## Drill
Zone Map & Pushdown Optimization Drill #5

## Solution SQL

```sql
SELECT
    device_id, timestamp,
    Filter on sorted timestamp prefix
FROM sensor_readings
GROUP BY device_id, timestamp
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `device_id, timestamp` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
