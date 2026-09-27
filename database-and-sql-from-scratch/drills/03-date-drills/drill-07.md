# Drill 07: Year-over-Year / Year Selection

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Extract the year from order_date and count total orders by year. Project order_year and total_orders. Order by order_year ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per year.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-07.md
```
