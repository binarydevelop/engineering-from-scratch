# Solution: DRILL-AGGR-11

## Drill
Fact Aggregation Drill #11

## Solution SQL

```sql
SELECT
    category, country,
    SUM(net_revenue), COUNT(*)
FROM fact_order_items
GROUP BY category, country
LIMIT 50;
```

## Physical Verification
- **Plan Operators**: `TableScan` -> `HashAggregate` -> `TopNSort`.
- **Projection**: Only `category, country` and measures referenced are deserialized.
- **Memory Invariant**: Aggregation state bounded by grouping cardinality.
