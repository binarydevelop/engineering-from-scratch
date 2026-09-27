# Exercise Q97: Q97 Window Running Total Frames

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `ROWS BETWEEN`  

---

## 1. Business Requirement

> Compute cumulative completed revenue using explicit window frame: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. Project order_id, order_date, total_amount, cumulative_revenue. Order by order_date ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_id, order_date, total_amount, cumulative_revenue

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
python3 scripts/grade-query.py exercises/advanced/q97-window-running-total-frames.md
```
