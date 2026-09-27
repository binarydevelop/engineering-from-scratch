# Drill 01: Scalar Subquery in WHERE

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find all products with price strictly higher than the average price across all products. Project name and price. Order by price DESC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per above-average priced product.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-01.md
```
