# Exercise Q105: Q105 Pivot Revenue By Month Category

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Pivot`, `Conditional Aggregate`  

---

## 1. Business Requirement

> Pivot revenue for 2026: columns for category_name, jan_revenue, feb_revenue, mar_revenue. Order by category_name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: category_name, jan_revenue, feb_revenue, mar_revenue

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
python3 scripts/grade-query.py exercises/advanced/q105-pivot-revenue-by-month-category.md
```
