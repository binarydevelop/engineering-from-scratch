# Exercise Q57: Q57 Banking Account Reconciliation

**Tier:** Intermediate  
**Target Schema:** `banking`  
**Concept Tags:** `Banking`, `Financial Invariants`  

---

## 1. Business Requirement

> Verify double-entry integrity: compute sum of debits and sum of credits for each transaction. Confirm (sum_debit - sum_credit) equals 0.00 for all settled transactions. Order by transaction_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: transaction_id, total_debit, total_credit, delta

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
python3 scripts/grade-query.py exercises/intermediate/q57-banking-account-reconciliation.md
```
