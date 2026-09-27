# Exercise Q34: Q34 Sum Total Revenue

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Aggregate`, `SUM`  

---

## 1. Business Requirement

> Calculate total gross revenue of all completed orders. Aliased as gross_revenue.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 1 column: gross_revenue

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
python3 scripts/grade-query.py exercises/beginner/q34-sum-total-revenue.md
```
