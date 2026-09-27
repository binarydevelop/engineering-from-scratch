# Drill 07: Min and Max per Category

**Category:** 02-group-by-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find min price and max price of products in each category. Project category_id, min_price, max_price. Order by category_id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per category.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-07.md
```
