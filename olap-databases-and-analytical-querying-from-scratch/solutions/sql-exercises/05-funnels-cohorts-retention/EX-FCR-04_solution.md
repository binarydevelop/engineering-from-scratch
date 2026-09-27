# Solution: EX-FCR-04

## Business Requirement
Multi-Stage Conversion Funnel and User Cohort Retention Drill #4

## Verified SQL Solution (DuckDB)

```sql
SELECT
    COUNT(DISTINCT user_id) AS total_visitors,
    COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS step_1_view,
    COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) AS step_2_cart,
    COUNT(DISTINCT CASE WHEN event_type = 'checkout_start' THEN user_id END) AS step_3_checkout,
    COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS step_4_purchase,
    ROUND(COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) * 100.0 / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS overall_conversion_pct
FROM web_events;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `user_id, event_type, event_time` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate -> ConditionalAggregation`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `3` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
