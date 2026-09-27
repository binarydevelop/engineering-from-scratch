# Exercise Q104: Q104 Day 1 7 30 Retention Concept

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Retention`, `Intervals`  

---

## 1. Business Requirement

> Count users who logged back in exactly within 7 days of their first seen date. Project first_seen_date, total_users, retained_7d. Order by first_seen_date ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: first_seen_date, total_users, retained_7d

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
python3 scripts/grade-query.py exercises/advanced/q104-day-1-7-30-retention-concept.md
```
