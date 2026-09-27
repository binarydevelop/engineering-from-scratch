# Solution: DRILL-RETE-09

## Drill
N-Day Activity Retention Drill #9

## Solution SQL

```sql
SELECT
    user_id, event_time,
    COUNT(DISTINCT user_id) active on Day N
FROM web_events
GROUP BY user_id, event_time
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `user_id, event_time` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
