# Exercise Q06: Q06 Filter Compound Or And

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `WHERE`, `Boolean Logic`  

---

## 1. Business Requirement

> Find products where category_id is 2 OR category_id is 3, AND price is strictly under 500.00. Mind operator precedence! Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 3 rows, 3 columns: id, category_id, name, price

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
python3 scripts/grade-query.py exercises/beginner/q06-filter-compound-or-and.md
```
