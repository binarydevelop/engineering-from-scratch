# Exercise Q66: Q66 Daily Active Users

**Tier:** Intermediate  
**Target Schema:** `analytics`  
**Concept Tags:** `Analytics`, `DAU`  

---

## 1. Business Requirement

> Calculate Daily Active Users (count of distinct user_id) per calendar day from the events table. Order by event_day ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: event_day, dau

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
python3 scripts/grade-query.py exercises/intermediate/q66-daily-active-users.md
```
