# Solution: DRILL-COHO-07

## Drill
User Acquisition Cohort Drill #7

## Solution SQL

```sql
SELECT
    signup_date, created_at,
    COUNT(DISTINCT user_id)
FROM dim_users JOIN fact_order_items
GROUP BY signup_date, created_at
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `signup_date, created_at` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
