# Exercise Q26: Q26 Boolean Logic Matrix

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Logic`, `Three-Valued`  

---

## 1. Business Requirement

> Inspect the truth table of NULL comparison: evaluate (NULL = NULL) IS NULL, (NULL IS NULL), (TRUE AND NULL IS NULL).

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 3 columns: col1, col2, col3

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
python3 scripts/grade-query.py exercises/beginner/q26-boolean-logic-matrix.md
```
