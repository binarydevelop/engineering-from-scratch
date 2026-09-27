# Exercise Q119: Q119 Multi Tenant Data Isolation Check

**Tier:** Advanced  
**Target Schema:** `saas`  
**Concept Tags:** `Multi-Tenancy`, `Security`  

---

## 1. Business Requirement

> Write a multi-tenant query ensuring user 1 (Acme Corp) only accesses projects belonging to organization 1. Return project_id, project_name. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, name

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
python3 scripts/grade-query.py exercises/advanced/q119-multi-tenant-data-isolation-check.md
```
