# Exercise Q56: Q56 Saas Seat Utilization

**Tier:** Intermediate  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Calculations`  

---

## 1. Business Requirement

> Find organizations where used memberships exceed 80% of purchased subscription seats. Project org name, seats_used, seats_purchased, utilization_pct. Order by utilization_pct DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: name, seats_used, seats_purchased, utilization_pct

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
python3 scripts/grade-query.py exercises/intermediate/q56-saas-seat-utilization.md
```
