# Exercise Q25: Q25 Safe Update Returning

**Tier:** Beginner  
**Target Schema:** `banking`  
**Concept Tags:** `DML`, `RETURNING`  

---

## 1. Business Requirement

> Write a SELECT showing what an account balance would look like after adding 500 interest to checking accounts (account_type = 'checking'). Project id, account_number, balance, new_balance. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 4 rows, 4 columns: id, account_number, balance, new_balance

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
python3 scripts/grade-query.py exercises/beginner/q25-safe-update-returning.md
```
