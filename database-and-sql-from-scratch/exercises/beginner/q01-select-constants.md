# Exercise Q01: Q01 Select Constants

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `SELECT`, `Expressions`  

---

## 1. Business Requirement

> Select literal numbers and strings: return 42 as answer, 'PostgreSQL 16' as engine, and 100 * 1.05 as taxed_amount.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 3 columns: answer (int), engine (text), taxed_amount (numeric)

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
python3 scripts/grade-query.py exercises/beginner/q01-select-constants.md
```
