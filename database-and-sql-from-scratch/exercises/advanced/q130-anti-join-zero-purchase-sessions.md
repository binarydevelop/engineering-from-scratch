# Exercise Q130: Q130 Anti Join Zero Purchase Sessions

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Anti-Join`, `Sessions`  

---

## 1. Business Requirement

> Find sessions that viewed products but never reached checkout. Project session id and user_id. Order by session id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: session_id, user_id

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
python3 scripts/grade-query.py exercises/advanced/q130-anti-join-zero-purchase-sessions.md
```
