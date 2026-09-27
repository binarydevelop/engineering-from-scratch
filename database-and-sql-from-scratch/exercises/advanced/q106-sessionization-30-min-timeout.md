# Exercise Q106: Q106 Sessionization 30 Min Timeout

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Sessionization`, `Window LAG`  

---

## 1. Business Requirement

> Reconstruct user browsing sessions: if duration between consecutive events exceeds 30 minutes, flag new session start (is_new_session = 1). Project user_id, event_timestamp, is_new_session. Order by user_id ASC, event_timestamp ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: user_id, event_timestamp, is_new_session

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
python3 scripts/grade-query.py exercises/advanced/q106-sessionization-30-min-timeout.md
```
