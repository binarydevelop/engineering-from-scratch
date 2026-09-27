# Exercise Q122: Q122 Window Range Vs Rows Difference

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `RANGE vs ROWS`  

---

## 1. Business Requirement

> Demonstrate the critical difference between RANGE and ROWS frames when duplicate timestamps or values exist. Project order_id, total_amount, rows_sum, range_sum. Order by total_amount ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, total_amount, rows_sum, range_sum

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
python3 scripts/grade-query.py exercises/advanced/q122-window-range-vs-rows-difference.md
```
