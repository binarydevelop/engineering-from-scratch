# Drill 10: Filter with Filter Clause (Standard SQL FILTER)

**Category:** 02-group-by-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Using SQL standard FILTER (WHERE ...), calculate total count of orders, count of completed orders, and count of refunded orders by customer_id. Order by customer_id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-10.md
```
