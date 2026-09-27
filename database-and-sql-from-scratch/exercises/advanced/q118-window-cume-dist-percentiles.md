# Exercise Q118: Q118 Window Cume Dist Percentiles

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `CUME_DIST`  

---

## 1. Business Requirement

> Calculate cumulative distribution CUME_DIST() of order totals. Project id, total_amount, cume_dist_val. Order by total_amount ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, total_amount, cume_dist_val

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
python3 scripts/grade-query.py exercises/advanced/q118-window-cume-dist-percentiles.md
```
