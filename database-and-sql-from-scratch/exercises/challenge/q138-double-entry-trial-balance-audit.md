# Exercise Q138: Q138 Double Entry Trial Balance Audit

**Tier:** Challenge  
**Target Schema:** `banking`  
**Concept Tags:** `Banking`, `Accounting`  

---

## 1. Business Requirement

> Generate a complete General Ledger Trial Balance: for every account, calculate net balance from ledger entries (Credits - Debits or Debits - Credits per account type) and verify that overall debits equal overall credits across the entire institution.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: total_system_debits, total_system_credits, system_balance_delta

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
python3 scripts/grade-query.py exercises/challenge/q138-double-entry-trial-balance-audit.md
```
