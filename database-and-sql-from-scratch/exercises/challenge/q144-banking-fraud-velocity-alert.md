# Exercise Q144: Q144 Banking Fraud Velocity Alert

**Tier:** Challenge  
**Target Schema:** `banking`  
**Concept Tags:** `Fraud Detection`, `Velocity`  

---

## 1. Business Requirement

> Detect potential financial fraud: accounts with 2 or more debit transactions occurring within 60 minutes of each other. Project account_id, txn1_id, txn2_id, minutes_delta. Order by account_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: account_id, txn1_id, txn2_id, minutes_delta

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
python3 scripts/grade-query.py exercises/challenge/q144-banking-fraud-velocity-alert.md
```
