# Drill 07: Cross Join (All Categories x Product Statuses)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Cross join root categories (parent_id IS NULL) with two statuses ('active', 'inactive'). Project category name and status. Order by category name, status.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per category-status permutation.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-07.md
```
