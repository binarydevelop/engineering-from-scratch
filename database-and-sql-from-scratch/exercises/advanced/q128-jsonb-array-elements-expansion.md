# Exercise Q128: Q128 Jsonb Array Elements Expansion

**Tier:** Advanced  
**Target Schema:** `saas`  
**Concept Tags:** `JSONB`, `jsonb_array_elements`  

---

## 1. Business Requirement

> Demonstrate JSONB array unnesting: if payload has tags array, expand with jsonb_array_elements_text. Return payload.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, payload

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
python3 scripts/grade-query.py exercises/advanced/q128-jsonb-array-elements-expansion.md
```
