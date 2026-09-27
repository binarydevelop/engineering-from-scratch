# Exercise Q13: Q13 Limit Offset Pagination

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `LIMIT`, `OFFSET`  

---

## 1. Business Requirement

> Fetch page 2 of products when sorted by price descending with page size of 3 items (i.e. items 4, 5, 6). Project id, name, price. Order by price DESC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 3 rows, 3 columns: id, name, price

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
python3 scripts/grade-query.py exercises/beginner/q13-limit-offset-pagination.md
```
