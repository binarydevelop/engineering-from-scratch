# Exercise Q141: Q141 Inventory Stockout Projection

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Inventory`, `Demand Forecasting`  

---

## 1. Business Requirement

> Forecast stockout risk: calculate average daily units sold over the last 60 days, and divide current stock_quantity by daily run rate to estimate days_until_stockout. Project sku, stock_quantity, days_until_stockout. Order by days_until_stockout ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: sku, stock_quantity, days_until_stockout

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
python3 scripts/grade-query.py exercises/challenge/q141-inventory-stockout-projection.md
```
