# Exercise Q154: Q154 Banking Audit Tamper Detection

**Tier:** Challenge  
**Target Schema:** `banking`  
**Concept Tags:** `Security`, `Integrity Hash`  

---

## 1. Business Requirement

> Audit ledger integrity: calculate running checksum / verification sum of transaction amounts per account. Project account_id, ledger_rows, net_ledger_amount, account_balance, is_reconciled. Order by account_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: account_id, ledger_rows, net_ledger_amount, balance, is_reconciled

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
python3 scripts/grade-query.py exercises/challenge/q154-banking-audit-tamper-detection.md
```
