# Exercise Q65: Q65 Multi Column Group With Totals

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `GROUP BY`, `Status Matrix`  

---

## 1. Business Requirement

> Summarize orders by year and status: return order_year, status, count of orders, and sum of total_amount. Order by order_year ASC, status ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_year, status, order_count, total_sum

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
python3 scripts/grade-query.py exercises/intermediate/q65-multi-column-group-with-totals.md
```
