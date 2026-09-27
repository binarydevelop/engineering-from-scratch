# Exercise Q78: Q78 Saas User Role Distribution

**Tier:** Intermediate  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Role Matrix`  

---

## 1. Business Requirement

> Count the number of users holding each role ('owner', 'admin', 'member') across all organizations. Order by role ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: role, count

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
python3 scripts/grade-query.py exercises/intermediate/q78-saas-user-role-distribution.md
```
