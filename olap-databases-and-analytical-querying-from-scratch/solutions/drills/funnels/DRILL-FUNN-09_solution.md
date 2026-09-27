# Solution: DRILL-FUNN-09

## Drill
Multi-Step Funnel Conversion Drill #9

## Solution SQL

```sql
SELECT
    event_type,
    COUNT(DISTINCT user_id)
FROM web_events
GROUP BY event_type
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `event_type` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
