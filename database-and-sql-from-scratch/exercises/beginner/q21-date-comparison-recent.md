# Exercise Q21: Q21 Date Comparison Recent

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Dates`, `Intervals`  

---

## 1. Business Requirement

> Find orders placed on or after '2026-02-01'. Return id, status, total_amount, order_date. Order by order_date ASC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 12 rows, 4 columns: id, status, total_amount, order_date

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
python3 scripts/grade-query.py exercises/beginner/q21-date-comparison-recent.md
```
