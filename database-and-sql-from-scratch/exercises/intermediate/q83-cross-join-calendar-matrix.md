# Exercise Q83: Q83 Cross Join Calendar Matrix

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `CROSS JOIN`, `Matrix`  

---

## 1. Business Requirement

> Create a reporting skeleton: CROSS JOIN distinct order years (2026) with distinct product categories. Count actual orders matching that year and category. Order by category name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: category_name, order_count

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
python3 scripts/grade-query.py exercises/intermediate/q83-cross-join-calendar-matrix.md
```
