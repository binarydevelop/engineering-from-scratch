# Exercise Q40: Q40 Scalar Subquery Where

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Subquery`, `Scalar`  

---

## 1. Business Requirement

> Find all products priced higher than the product named 'Precision Coffee Grinder'. Project name, price. Order by price DESC.

---

## 2. Expected Output Shape

- **Result Grain:** 6 rows, 2 columns: name, price

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
python3 scripts/grade-query.py exercises/beginner/q40-scalar-subquery-where.md
```
