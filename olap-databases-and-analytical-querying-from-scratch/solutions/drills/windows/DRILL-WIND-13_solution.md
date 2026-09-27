# Solution: DRILL-WIND-13

## Drill
Window Frame & Partition Drill #13

## Solution SQL

```sql
SELECT
    user_id, event_time,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time)
FROM web_events
GROUP BY user_id, event_time
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `user_id, event_time` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
