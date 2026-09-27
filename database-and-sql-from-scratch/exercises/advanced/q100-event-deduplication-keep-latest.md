# Exercise Q100: Q100 Event Deduplication Keep Latest

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Deduplication`, `ROW_NUMBER`  

---

## 1. Business Requirement

> Given potential duplicate events per session and event_name, select ONLY the latest occurrence. Project session_id, event_name, event_timestamp. Order by session_id ASC, event_timestamp ASC.

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
python3 scripts/grade-query.py exercises/advanced/q100-event-deduplication-keep-latest.md
```
