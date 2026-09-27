# Exercise Q85: Q85 Banking High Risk Customers

**Tier:** Intermediate  
**Target Schema:** `banking`  
**Concept Tags:** `Risk Analysis`, `WHERE`  

---

## 1. Business Requirement

> Find customers with risk_score >= 70 who hold more than $100 in checking balance. Project customer name, tax_id, risk_score, balance. Order by risk_score DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: full_name, tax_id, risk_score, balance

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
python3 scripts/grade-query.py exercises/intermediate/q85-banking-high-risk-customers.md
```
