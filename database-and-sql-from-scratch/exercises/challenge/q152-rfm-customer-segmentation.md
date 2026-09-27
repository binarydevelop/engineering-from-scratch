# Exercise Q152: Q152 Rfm Customer Segmentation

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Analytics`, `RFM Segmentation`  

---

## 1. Business Requirement

> Build an RFM (Recency, Frequency, Monetary) segmentation model: calculate Recency (days since last order), Frequency (total completed orders), and Monetary (total spent). Order by monetary DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, recency_days, frequency, monetary

---

## 3. Query Thinking Framework Checklist

Before writing SQL, answer these questions:
1. What should one row represent in your output?
2. Which tables hold the primary facts and attributes?
3. What is the join cardinality? (1:1, 1:N, N:M)
4. Are any rows eliminated by NULL handling or outer joins?
5. Is an explicit `ORDER BY` necessary for deterministic result verification?

---

## 4. Verification

Execute your query and grade it against the reference solution:

```bash
python3 scripts/grade-query.py exercises/challenge/q152-rfm-customer-segmentation.md
```
