# Exercise Q95: Q95 Window Lag Mom Revenue Delta

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `LAG`, `MoM Growth`  

---

## 1. Business Requirement

> Calculate Month-over-Month revenue change: compute monthly completed revenue, previous month revenue via LAG, and dollar delta. Order by order_month ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_month, monthly_rev, prev_month_rev, dollar_delta

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
python3 scripts/grade-query.py exercises/advanced/q95-window-lag-mom-revenue-delta.md
```
