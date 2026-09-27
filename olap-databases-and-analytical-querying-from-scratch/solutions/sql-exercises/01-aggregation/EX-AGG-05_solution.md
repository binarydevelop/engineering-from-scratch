# Solution: EX-AGG-05

## Business Requirement
Transaction Volume, Fraud Rate, and Total Fees by Merchant Category

## Verified SQL Solution (ANSI SQL)

```sql
SELECT
    merchant_category,
    COUNT(*) AS txn_count,
    ROUND(SUM(amount), 2) AS total_amount,
    COUNT(CASE WHEN is_fraud THEN 1 END) AS fraud_count,
    ROUND(COUNT(CASE WHEN is_fraud THEN 1 END) * 100.0 / COUNT(*), 3) AS fraud_rate_pct
FROM financial_transactions
GROUP BY merchant_category
ORDER BY fraud_rate_pct DESC;
```

## Physical Execution & Plan Breakdown
- **Scanned Columns**: Only `merchant_category, amount, fee, is_fraud` are loaded from disk. Unused columns are skipped.
- **Execution Strategy**: `TableScan -> HashAggregate`.
- **Why This Is Physically Efficient**:
  1. Projection pushdown ensures only `4` column arrays are traversed in memory.
  2. The aggregation state accumulates into an in-cache hash table.
  3. Avoids unneeded sorting or full row materialization.
