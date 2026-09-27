# Exercise Q89: Q89 Null Safe Equality Is Not Distinct

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Standard SQL`, `IS NOT DISTINCT FROM`  

---

## 1. Business Requirement

> Compare two queries: select categories where parent_id = NULL vs parent_id IS NOT DISTINCT FROM NULL. Demonstrate standard SQL NULL-safe equality.

---

## 2. Expected Output Shape

- **Result Grain:** 3 rows: id, name, parent_id

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
python3 scripts/grade-query.py exercises/intermediate/q89-null-safe-equality-is-not-distinct.md
```
