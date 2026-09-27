# Exercise Q133: Q133 Rolling Seven Day Revenue

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Rolling Scaffolding`  

---

## 1. Business Requirement

> Calculate rolling 7-day revenue for every calendar day in January 2026. Use generate_series to guarantee no missing dates. Order by calendar_day ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: calendar_day, daily_revenue, rolling_7d_revenue

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
python3 scripts/grade-query.py exercises/challenge/q133-rolling-seven-day-revenue.md
```
