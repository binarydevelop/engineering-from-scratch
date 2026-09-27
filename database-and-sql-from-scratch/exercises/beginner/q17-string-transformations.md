# Exercise Q17: Q17 String Transformations

**Tier:** Beginner  
**Target Schema:** `social`  
**Concept Tags:** `Strings`, `LOWER/UPPER/LENGTH`  

---

## 1. Business Requirement

> Return full_name in uppercase, username in lowercase, and length of bio (or 0 if null) for all users. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 7 rows, 4 columns: id, upper_name, lower_username, bio_len

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
python3 scripts/grade-query.py exercises/beginner/q17-string-transformations.md
```
