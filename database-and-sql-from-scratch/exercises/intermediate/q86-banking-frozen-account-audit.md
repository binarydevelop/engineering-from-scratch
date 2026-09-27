# Exercise Q86: Q86 Banking Frozen Account Audit

**Tier:** Intermediate  
**Target Schema:** `banking`  
**Concept Tags:** `Audit`, `Status`  

---

## 1. Business Requirement

> List all frozen accounts, their owner's name, and current balance. Order by balance DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: account_number, full_name, balance

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
python3 scripts/grade-query.py exercises/intermediate/q86-banking-frozen-account-audit.md
```
