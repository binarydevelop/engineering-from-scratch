# Exercise Q115: Q115 Complex Reporting Rolling Revenue

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Rolling 30-Day Window`  

---

## 1. Business Requirement

> For each day with completed orders, calculate daily revenue and rolling 30-day cumulative revenue using window range. Order by order_day ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_day, daily_rev, rolling_30d_rev

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
python3 scripts/grade-query.py exercises/advanced/q115-complex-reporting-rolling-revenue.md
```
