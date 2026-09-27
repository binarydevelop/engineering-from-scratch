# Query Requirement: EX-INT-055 (Intermediate Tier #55)

## Business Question
What is the optimal query for access pattern #125 in Apache Cassandra?
"Retrieve the top 20 business records for customer `CUST-0055` matching operational status `CONFIRMED` between timestamp `2026-09-01` and `2026-09-25`."

---

## Expected Result Shape
```json
[
  {
    "record_id": "REC-00055",
    "entity_key": "CUST-0055",
    "status": "CONFIRMED",
    "timestamp": "2026-09-20T14:30:00Z",
    "amount": 127.5
  }
]
```

---

## Access Pattern
* **Pattern ID:** `AP-INT-055`
* **Database Engine:** Apache Cassandra
* **Throughput SLA:** 3,500 QPS, p99 < 12ms
* **Input Parameters:** `customer_id = 'CUST-0055'`, date range, limit 20

---

## Dataset
* **Domain:** E-Commerce & Transaction Ledger (`datasets/ecommerce/orders.json`)
* **Collection / Table:** `orders` / `orders_by_customer`

---

## Data Model
* **Partition Key / Primary Key:** `customer_id`
* **Sort Key / Clustering Column:** `created_at DESC`
* **Attributes / Fields:** `order_id`, `status`, `total_amount`, `items`

---

## Indexes
* **Index Specification:** `{"customer_id": 1, "created_at": -1, "status": 1}`

---

## Query
```text
-- Formulate your Apache Cassandra query here following QUERY_TEMPLATE.md
```

---

## Prediction
* **Expected Partitions Touched:** 1 physical partition
* **Expected Index Behavior:** Direct index leaf seek on primary / secondary index
* **Records Scanned:** Exactly 20 records

---

## Expected Partitions Touched
* Single partition node based on `hash(customer_id)`. Zero scatter-gather fan-out.

---

## Expected Index Behavior
* B-Tree / SSTable index bounds: `customer_id == "CUST-0055"`, reverse chronological order.

---

## Actual Result
*(Execute against local container and record results)*

---

## Explain / Query Plan
```json
{
  "stage": "IXSCAN",
  "keysExamined": 20,
  "docsExamined": 20
}
```

---

## Measurements
* **Execution Latency:** < 2.5ms
* **Read Amplification:** 1.0

---

## Edge Cases
1. Customer has 0 orders: Returns empty set in sub-millisecond time.
2. Skewed customer with 100,000 orders: Handled by limit(20) without scanning entire partition.

---

## Scale Concerns
Ensure embedding does not exceed document size limits (16MB BSON or 400KB DynamoDB item limit).

---

## Alternative Model
* Wide-Column CQL Table: `orders_by_customer` with clustering column `created_at DESC`.

---

## Alternative Database
* DynamoDB: `PK=CUST#id`, `SK=ORD#timestamp`.

---

## SQL Comparison
```sql
SELECT * FROM orders WHERE customer_id = 'CUST-0055' AND status = 'CONFIRMED' ORDER BY created_at DESC LIMIT 20;
```

---

## Explanation
Query executes in $O(\log N + K)$ time by navigating directly to the customer's partition and reading contiguous records from physical storage.
