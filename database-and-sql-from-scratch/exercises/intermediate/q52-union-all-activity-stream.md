# Exercise Q52: Q52 Union All Activity Stream

**Tier:** Intermediate  
**Target Schema:** `social`  
**Concept Tags:** `Set Operations`, `UNION ALL`  

---

## 1. Business Requirement

> Create a unified activity feed combining posts and comments. Return user_id, activity_type ('post' or 'comment'), content_snippet (SUBSTRING text 1 to 30), and created_at. Order by created_at DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: user_id, activity_type, content_snippet, created_at

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
python3 scripts/grade-query.py exercises/intermediate/q52-union-all-activity-stream.md
```
