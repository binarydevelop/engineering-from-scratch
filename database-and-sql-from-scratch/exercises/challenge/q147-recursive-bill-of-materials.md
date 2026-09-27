# Exercise Q147: Q147 Recursive Bill Of Materials

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Recursive CTE`, `BOM`  

---

## 1. Business Requirement

> Calculate total catalog depth and count of leaf subcategories beneath root category 'Electronics' (id = 1). Return total_subcategories, max_depth.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: total_subcategories, max_depth

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
python3 scripts/grade-query.py exercises/challenge/q147-recursive-bill-of-materials.md
```
