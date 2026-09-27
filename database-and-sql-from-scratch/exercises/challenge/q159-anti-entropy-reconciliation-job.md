# Exercise Q159: Q159 Anti Entropy Reconciliation Job

**Tier:** Challenge  
**Target Schema:** `banking`  
**Concept Tags:** `Audit`, `Anti-Entropy`  

---

## 1. Business Requirement

> Reconciliation job: detect any settled transaction where the sum of ledger entries does not match transaction amount. Project transaction_id, txn_amount, ledger_debit_sum, is_balanced.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: transaction_id, amount, ledger_debit_sum, is_balanced

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
python3 scripts/grade-query.py exercises/challenge/q159-anti-entropy-reconciliation-job.md
```
