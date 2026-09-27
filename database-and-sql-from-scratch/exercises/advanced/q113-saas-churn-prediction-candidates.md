# Exercise Q113: Q113 Saas Churn Prediction Candidates

**Tier:** Advanced  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Churn Heuristics`  

---

## 1. Business Requirement

> Flag churn risk organizations: organizations whose subscription is active or past_due, but have generated 0 telemetry events in the last 30 days. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, name, status

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
python3 scripts/grade-query.py exercises/advanced/q113-saas-churn-prediction-candidates.md
```
