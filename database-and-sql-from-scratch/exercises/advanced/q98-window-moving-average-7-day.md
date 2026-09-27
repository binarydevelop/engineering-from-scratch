# Exercise Q98: Q98 Window Moving Average 7 Day

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Moving Average`  

---

## 1. Business Requirement

> Calculate moving average over last 3 completed orders (current and 2 preceding). Project order_id, total_amount, moving_avg. Order by order_date ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_id, total_amount, moving_avg

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
python3 scripts/grade-query.py exercises/advanced/q98-window-moving-average-7-day.md
```
