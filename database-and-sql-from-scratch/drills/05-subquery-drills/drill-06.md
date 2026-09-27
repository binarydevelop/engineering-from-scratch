# Drill 06: Multi-Stage CTE Pipeline

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Using two CTEs: 1. `order_totals` (customer_id, total_spent), 2. `ranked` (customer_id, total_spent, rank by spend). Return top 3 spenders. Order by rank ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per top 3 customer.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-06.md
```
