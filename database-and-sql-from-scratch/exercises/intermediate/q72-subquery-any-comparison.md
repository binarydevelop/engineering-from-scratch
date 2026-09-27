# Exercise Q72: Q72 Subquery Any Comparison

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Subquery`, `ANY Operator`  

---

## 1. Business Requirement

> Find products whose price matches ANY product price in category 8 (Books). Project name, price. Order by price ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: name, price

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
python3 scripts/grade-query.py exercises/intermediate/q72-subquery-any-comparison.md
```
