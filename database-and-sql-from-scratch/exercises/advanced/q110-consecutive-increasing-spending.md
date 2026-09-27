# Exercise Q110: Q110 Consecutive Increasing Spending

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Trend Detection`  

---

## 1. Business Requirement

> Identify customers whose order amounts increased across two consecutive completed orders. Use LAG. Project customer_id, order_a_val, order_b_val. Order by customer_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, prev_amount, curr_amount

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
python3 scripts/grade-query.py exercises/advanced/q110-consecutive-increasing-spending.md
```
