# Solution: DRILL-QUER-04

## Drill
Execution Plan Analysis Drill #4

## Solution SQL

```sql
SELECT
    country,
    EXPLAIN ANALYZE SELECT country, SUM(net_revenue)
FROM fact_order_items
GROUP BY country
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `country` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
