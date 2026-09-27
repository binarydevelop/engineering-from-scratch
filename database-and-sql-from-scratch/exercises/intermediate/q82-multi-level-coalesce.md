# Exercise Q82: Q82 Multi Level Coalesce

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `NULL`, `Fallbacks`  

---

## 1. Business Requirement

> Display product contact support hierarchy: return product name, category slug, and a fallback support contact 'support@' || category slug || '.com'. Order by product name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: name, slug, support_email

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
python3 scripts/grade-query.py exercises/intermediate/q82-multi-level-coalesce.md
```
