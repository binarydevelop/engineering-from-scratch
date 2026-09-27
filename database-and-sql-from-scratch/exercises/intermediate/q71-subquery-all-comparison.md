# Exercise Q71: Q71 Subquery All Comparison

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Subquery`, `ALL Operator`  

---

## 1. Business Requirement

> Find products whose price is strictly greater than ALL products in category 3 (Audio). Project name, price. Order by price ASC.

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
python3 scripts/grade-query.py exercises/intermediate/q71-subquery-all-comparison.md
```
