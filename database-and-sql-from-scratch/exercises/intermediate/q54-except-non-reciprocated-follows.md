# Exercise Q54: Q54 Except Non Reciprocated Follows

**Tier:** Intermediate  
**Target Schema:** `social`  
**Concept Tags:** `Set Operations`, `EXCEPT`  

---

## 1. Business Requirement

> Find users whom user 1 follows, who DO NOT follow user 1 back. Return following_id. Order by following_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: following_id

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
python3 scripts/grade-query.py exercises/intermediate/q54-except-non-reciprocated-follows.md
```
