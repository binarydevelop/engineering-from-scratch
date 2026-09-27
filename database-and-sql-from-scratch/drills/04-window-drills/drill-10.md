# Drill 10: NTILE (Quartile Distribution)

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Divide products into 4 price quartiles using NTILE(4). Project name, price, quartile. Order by price ASC, name ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per product.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-10.md
```
