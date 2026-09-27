# Drill 03: Group By with HAVING Filter

**Category:** 02-group-by-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find customers who have placed 2 or more completed orders. Return customer_id and order_count. Order by order_count DESC, customer_id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per qualifying customer.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-03.md
```
