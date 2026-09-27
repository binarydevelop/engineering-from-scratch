# Exercise Q05: Q05 Filter Price Range

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `WHERE`, `BETWEEN`  

---

## 1. Business Requirement

> Find all products with price between 100.00 and 500.00 inclusive. Project sku, name, price. Order by price ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 3 rows, 3 columns: sku, name, price

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
python3 scripts/grade-query.py exercises/beginner/q05-filter-price-range.md
```
