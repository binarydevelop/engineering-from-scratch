# Exercise Q28: Q28 Substring Extraction

**Tier:** Beginner  
**Target Schema:** `banking`  
**Concept Tags:** `Strings`, `SUBSTRING`  

---

## 1. Business Requirement

> Extract the 3-letter account category code from account_number (e.g. 'CHK' from 'ACCT-CHK-10001'). Return id, account_number, acct_code. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 5 rows, 3 columns: id, account_number, acct_code

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
python3 scripts/grade-query.py exercises/beginner/q28-substring-extraction.md
```
