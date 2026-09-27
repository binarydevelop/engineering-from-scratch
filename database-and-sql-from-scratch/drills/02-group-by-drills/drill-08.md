# Drill 08: Group By Expression (Price Range Bucket)

**Category:** 02-group-by-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Group products into buckets: '< 100', '100-500', '> 500'. Count products per bucket. Order by product_count DESC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per price bucket.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-08.md
```
