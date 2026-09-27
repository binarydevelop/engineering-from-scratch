# Exercise Q47: Q47 Correlated Subquery Dept Avg

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Subquery`, `Correlated`  

---

## 1. Business Requirement

> Find products that are priced strictly higher than the average price of all products in their own category. Return category_id, name, price. Order by category_id ASC, price DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows per category: category_id, name, price

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
python3 scripts/grade-query.py exercises/intermediate/q47-correlated-subquery-dept-avg.md
```
