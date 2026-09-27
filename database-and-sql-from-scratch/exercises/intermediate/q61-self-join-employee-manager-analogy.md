# Exercise Q61: Q61 Self Join Employee Manager Analogy

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Self Join`, `Hierarchies`  

---

## 1. Business Requirement

> List all categories along with their grandparent category name (parent of parent) if applicable. Project category_name, parent_name, grandparent_name. Order by category_name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: category_name, parent_name, grandparent_name

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
python3 scripts/grade-query.py exercises/intermediate/q61-self-join-employee-manager-analogy.md
```
