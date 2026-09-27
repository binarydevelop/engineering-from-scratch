# Drill 02: Correlated Subquery in WHERE

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find products whose price is strictly greater than the average price of products in their OWN category. Project category_id, name, price. Order by category_id ASC, price DESC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per qualifying product.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-02.md
```
