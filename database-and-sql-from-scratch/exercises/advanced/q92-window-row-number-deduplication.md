# Exercise Q92: Q92 Window Row Number Deduplication

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Window`, `ROW_NUMBER`, `Deduplication`  

---

## 1. Business Requirement

> In event clickstream, find the FIRST event recorded for each session_id using ROW_NUMBER. Project session_id, event_name, event_timestamp. Order by session_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: session_id, event_name, event_timestamp

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
python3 scripts/grade-query.py exercises/advanced/q92-window-row-number-deduplication.md
```
