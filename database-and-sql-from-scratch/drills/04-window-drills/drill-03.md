# Drill 03: DENSE_RANK (Top Products by Price)

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Assign dense price rank to products within each category_id. Project category_id, name, price, price_rank. Order by category_id ASC, price_rank ASC, name ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per product.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-03.md
```
