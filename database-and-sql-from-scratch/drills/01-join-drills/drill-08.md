# Drill 08: Left Anti-Join (Unsold Products)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find products that have NEVER been ordered. Select product id, sku, and name. Order by product id ascending.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per unsold product.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-08.md
```
