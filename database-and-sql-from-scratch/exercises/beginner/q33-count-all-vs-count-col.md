# Exercise Q33: Q33 Count All Vs Count Col

**Tier:** Beginner  
**Target Schema:** `social`  
**Concept Tags:** `Aggregate`, `COUNT`  

---

## 1. Business Requirement

> Demonstrate COUNT(*) vs COUNT(bio) in users table. Return total_users and users_with_bio.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 2 columns: total_users, users_with_bio

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
python3 scripts/grade-query.py exercises/beginner/q33-count-all-vs-count-col.md
```
