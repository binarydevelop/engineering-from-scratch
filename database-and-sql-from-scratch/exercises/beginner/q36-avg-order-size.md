# Exercise Q36: Q36 Avg Order Size

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Aggregate`, `AVG`  

---

## 1. Business Requirement

> Calculate the average total amount for completed orders, rounded to 2 decimal places. Aliased as avg_order_val.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 1 column: avg_order_val

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
python3 scripts/grade-query.py exercises/beginner/q36-avg-order-size.md
```
