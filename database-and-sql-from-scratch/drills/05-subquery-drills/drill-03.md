# Drill 03: EXISTS (Customers with Completed Orders)

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find customers who have at least one completed order using EXISTS. Project customer id and email. Order by customer id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-03.md
```
