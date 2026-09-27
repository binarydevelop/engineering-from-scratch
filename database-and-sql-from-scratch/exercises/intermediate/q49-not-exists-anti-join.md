# Exercise Q49: Q49 Not Exists Anti Join

**Tier:** Intermediate  
**Target Schema:** `social`  
**Concept Tags:** `NOT EXISTS`, `Anti-Join`  

---

## 1. Business Requirement

> Find users who have NEVER posted anything and NEVER liked any posts. Project id, username. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Lurker users: id, username

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
python3 scripts/grade-query.py exercises/intermediate/q49-not-exists-anti-join.md
```
