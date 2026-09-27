# Exercise Q107: Q107 Customer Lifetime Value Distribution

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `LTV`, `Percentiles`  

---

## 1. Business Requirement

> Calculate Customer Lifetime Value (LTV) for completed orders, and divide customers into 3 LTV tiers: Top 20% ('VIP'), Middle 50% ('Core'), Bottom 30% ('Standard') using NTILE or PERCENT_RANK. Order by ltv DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, ltv, ltv_tier

---

## 3. Query Thinking Framework Checklist

Before writing SQL, answer these questions:
1. What should one row represent in your output?
2. Which tables hold the primary facts and attributes?
3. What is the join cardinality? (1:1, 1:N, N:M)
4. Are any rows eliminated by NULL handling or outer joins?
5. Is an explicit `ORDER BY` necessary for deterministic result verification?

---

## 4. Verification

Execute your query and grade it against the reference solution:

```bash
python3 scripts/grade-query.py exercises/advanced/q107-customer-lifetime-value-distribution.md
```
