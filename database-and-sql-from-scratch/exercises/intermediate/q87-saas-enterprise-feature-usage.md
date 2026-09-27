# Exercise Q87: Q87 Saas Enterprise Feature Usage

**Tier:** Intermediate  
**Target Schema:** `saas`  
**Concept Tags:** `JSONB`, `Feature Flag`  

---

## 1. Business Requirement

> Count how many times each feature flag has been enabled in 'settings.updated' events. Inspect payload->'feature_flags'. Return count.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: dark_mode_updates

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
python3 scripts/grade-query.py exercises/intermediate/q87-saas-enterprise-feature-usage.md
```
