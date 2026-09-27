# Drill 09: Top-2 Products per Category

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find top 2 most expensive products in each category. Project category_id, product name, price, rank. Order by category_id ASC, price DESC, name ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per product qualifying for top 2.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-09.md
```
