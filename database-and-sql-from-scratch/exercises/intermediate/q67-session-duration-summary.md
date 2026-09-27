# Exercise Q67: Q67 Session Duration Summary

**Tier:** Intermediate  
**Target Schema:** `analytics`  
**Concept Tags:** `Analytics`, `Sessions`  

---

## 1. Business Requirement

> Calculate duration of completed sessions in minutes (ended_at - started_at). Project session id, device_type, duration_minutes. Order by duration_minutes DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, device_type, duration_minutes

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
python3 scripts/grade-query.py exercises/intermediate/q67-session-duration-summary.md
```
