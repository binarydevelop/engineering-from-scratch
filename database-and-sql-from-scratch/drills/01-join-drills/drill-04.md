# Drill 04: Self-Join (Category Hierarchy)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select child category name and its parent category name. Only include categories that have a parent. Order by child name ascending.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per subcategory with a parent.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-04.md
```
