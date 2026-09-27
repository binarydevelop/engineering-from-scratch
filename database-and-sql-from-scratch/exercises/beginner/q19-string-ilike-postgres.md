# Exercise Q19: Q19 String Ilike Postgres

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Strings`, `ILIKE`  

---

## 1. Business Requirement

> Search products where name contains 'phone' case-insensitively using PostgreSQL ILIKE. Return id, name, sku. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 2 rows, 3 columns: id, name, sku

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
python3 scripts/grade-query.py exercises/beginner/q19-string-ilike-postgres.md
```
