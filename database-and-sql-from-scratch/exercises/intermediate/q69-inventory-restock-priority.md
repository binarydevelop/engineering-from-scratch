# Exercise Q69: Q69 Inventory Restock Priority

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Inventory`, `Stock Alert`  

---

## 1. Business Requirement

> Identify products where stock_quantity <= reorder_level. Project sku, product name, stock_quantity, reorder_level, and units_needed (reorder_level * 2 - stock_quantity). Order by units_needed DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: sku, name, stock_quantity, reorder_level, units_needed

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
python3 scripts/grade-query.py exercises/intermediate/q69-inventory-restock-priority.md
```
