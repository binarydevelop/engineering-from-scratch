# Exercise Q58: Q58 Banking Running Balance Audit

**Tier:** Intermediate  
**Target Schema:** `banking`  
**Concept Tags:** `Banking`, `Audit`  

---

## 1. Business Requirement

> Inspect ledger entries for account 1: verify if recorded running_balance matches the cumulative sum of credits minus debits. Project id, created_at, entry_type, amount, running_balance. Order by created_at ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, created_at, entry_type, amount, running_balance

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
python3 scripts/grade-query.py exercises/intermediate/q58-banking-running-balance-audit.md
```
