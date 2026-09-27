# Exercise Q157: Q157 Longest Inactivity Gap Per Customer

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Inactivity Gaps`  

---

## 1. Business Requirement

> For customers with multiple orders, find their maximum gap in days between two consecutive orders. Project customer_id, max_gap_days. Order by max_gap_days DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, max_gap_days

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
python3 scripts/grade-query.py exercises/challenge/q157-longest-inactivity-gap-per-customer.md
```
