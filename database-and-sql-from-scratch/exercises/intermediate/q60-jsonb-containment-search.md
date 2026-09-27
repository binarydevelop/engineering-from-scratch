# Exercise Q60: Q60 Jsonb Containment Search

**Tier:** Intermediate  
**Target Schema:** `saas`  
**Concept Tags:** `JSONB`, `GIN Containment`  

---

## 1. Business Requirement

> Find all events where payload contains key-value pair '"gpu": "h100"' using the @> JSONB containment operator. Project id, event_type, created_at. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, event_type, created_at

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
python3 scripts/grade-query.py exercises/intermediate/q60-jsonb-containment-search.md
```
