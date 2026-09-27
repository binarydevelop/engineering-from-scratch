# Exercise Q143: Q143 Session Referrer Attribution

**Tier:** Challenge  
**Target Schema:** `analytics`  
**Concept Tags:** `Marketing`, `Attribution`  

---

## 1. Business Requirement

> Multi-touch attribution: identify the first marketing campaign that touched each customer prior to their first purchase. Return user_id, acquisition_campaign. Order by user_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: user_id, acquisition_campaign

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
python3 scripts/grade-query.py exercises/challenge/q143-session-referrer-attribution.md
```
