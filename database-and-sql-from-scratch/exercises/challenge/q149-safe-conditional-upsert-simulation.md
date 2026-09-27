# Exercise Q149: Q149 Safe Conditional Upsert Simulation

**Tier:** Challenge  
**Target Schema:** `saas`  
**Concept Tags:** `DML`, `UPSERT Concept`  

---

## 1. Business Requirement

> Simulate an UPSERT query: using standard SQL CTEs, show existing organization record or prepare updated plan_tier = 'enterprise'. Project id, name, plan_tier.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, name, plan_tier

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
python3 scripts/grade-query.py exercises/challenge/q149-safe-conditional-upsert-simulation.md
```
