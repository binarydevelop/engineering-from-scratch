# Exercise Q09: Q09 Coalesce Handling

**Tier:** Beginner  
**Target Schema:** `social`  
**Concept Tags:** `NULL`, `COALESCE`  

---

## 1. Business Requirement

> Select username and a profile bio display. If bio is NULL, replace it with 'No bio provided.' aliased as display_bio. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 7 rows, 2 columns: username, display_bio

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
python3 scripts/grade-query.py exercises/beginner/q09-coalesce-handling.md
```
