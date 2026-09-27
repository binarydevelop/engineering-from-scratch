# Exercise Q64: Q64 Address Default Lookup

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `JOIN`, `Default Constraints`  

---

## 1. Business Requirement

> Find customers and their default shipping address city. If no default address exists, city should be 'No Default'. Project email, city. Order by email ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: email, city

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
python3 scripts/grade-query.py exercises/intermediate/q64-address-default-lookup.md
```
