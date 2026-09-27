# Drill 02: Left Join (Preserving Zero-Order Customers)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select customer id, email, and order id for all customers. If a customer has no orders, order id must be NULL. Order by customer id ascending, order id ascending nulls last.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer or order item relationship.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-02.md
```
