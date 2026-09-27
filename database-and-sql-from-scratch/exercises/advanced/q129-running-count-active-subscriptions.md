# Exercise Q129: Q129 Running Count Active Subscriptions

**Tier:** Advanced  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Active Subscriptions`  

---

## 1. Business Requirement

> Count currently active subscriptions vs trialing and past due subscriptions. Project status, sub_count, total_mrr. Order by status ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: status, sub_count, total_mrr

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
python3 scripts/grade-query.py exercises/advanced/q129-running-count-active-subscriptions.md
```
