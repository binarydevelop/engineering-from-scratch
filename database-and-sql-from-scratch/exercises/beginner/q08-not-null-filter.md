# Exercise Q08: Q08 Not Null Filter

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `NULL`, `IS NOT NULL`  

---

## 1. Business Requirement

> Find all subcategories that have an assigned parent_id. Return id, parent_id, name. Order by parent_id ASC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 5 rows, 3 columns: id, parent_id, name

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
python3 scripts/grade-query.py exercises/beginner/q08-not-null-filter.md
```
