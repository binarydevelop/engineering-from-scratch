# Drill 07: Recursive CTE (Category Breadcrumb Tree)

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Using a recursive CTE, build full category path for all categories (e.g. 'Electronics > Audio & Headphones'). Return id, path. Order by id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per category with hierarchical path.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-07.md
```
