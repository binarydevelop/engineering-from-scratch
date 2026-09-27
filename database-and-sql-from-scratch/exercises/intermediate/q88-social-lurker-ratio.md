# Exercise Q88: Q88 Social Lurker Ratio

**Tier:** Intermediate  
**Target Schema:** `social`  
**Concept Tags:** `Social`, `Ratios`  

---

## 1. Business Requirement

> Calculate the percentage of total users who have zero posts. Return total_users, lurker_count, lurker_pct.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: total_users, lurker_count, lurker_pct

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
python3 scripts/grade-query.py exercises/intermediate/q88-social-lurker-ratio.md
```
