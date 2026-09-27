# Query Requirement: [Query Identifier & Title]

## Business Question
[What commercial or user problem are we solving? e.g., "Find the latest 20 confirmed orders for customer CUST-1049, including total cost and item summaries."]

---

## Expected Result Shape
```json
[
  {
    "order_id": "ORD-9481",
    "created_at": "2026-09-25T06:14:00Z",
    "total_amount": 149.50,
    "status": "CONFIRMED",
    "item_count": 3
  }
]
```

---

## Access Pattern
* **Pattern ID:** `AP-042`
* **Trigger:** Customer visiting mobile order history page
* **Read / Write Ratio:** 98% Read / 2% Write
* **SLA:** p99 < 20ms at 5,000 QPS
* **Filter Predicates:** `customer_id = ? AND status = 'CONFIRMED'`
* **Ordering:** `created_at DESC`
* **Pagination:** Limit 20 with cursor

---

## Dataset
* **Domain:** E-Commerce / Orders Collection
* **Volume:** 50,000,000 documents (~45 GB)
* **Cardinality of Filter Key:** 2,500,000 unique customers (~20 orders/customer avg, max 10,000)

---

## Data Model
```json
{
  "_id": "ORD-9481",
  "customer_id": "CUST-1049",
  "status": "CONFIRMED",
  "created_at": "2026-09-25T06:14:00Z",
  "total_amount": 149.50,
  "items": [
    {"sku": "SKU-A", "qty": 2, "price": 49.75},
    {"sku": "SKU-B", "qty": 1, "price": 50.00}
  ]
}
```

---

## Key / Partition Key
* **Partition Key / Shard Key:** `customer_id` (Ensures all orders for a single customer live on the same physical partition)
* **Sort Key / Clustering Column:** `created_at DESC`

---

## Indexes
* **Primary Key:** `_id`
* **Secondary / Compound Index:** `{ customer_id: 1, created_at: -1, status: 1 }`

---

## Query
```javascript
// Native Query API / CQL / PartiQL / Cypher / Elasticsearch DSL
db.orders.find(
  { customer_id: "CUST-1049", status: "CONFIRMED" },
  { order_id: "$_id", created_at: 1, total_amount: 1, item_count: { $size: "$items" } }
)
.sort({ created_at: -1 })
.limit(20)
```

---

## Prediction
* **Expected Partitions Touched:** 1 partition (Targeted partition lookup via `customer_id`)
* **Expected Index Behavior:** Index-only scan on compound index (`customer_id`, `created_at`, `status`)
* **Scan Anticipation:** 0 collection scans; 20 keys examined, 20 documents fetched.

---

## Expected Partitions Touched
* Single partition node based on `hash(customer_id)`. Zero cluster broadcast fan-out.

---

## Expected Index Behavior
* B-Tree / SSTable index bounds: `customer_id == "CUST-1049"`, traversed in reverse chronological order, filtering on `status == "CONFIRMED"`.

---

## Actual Result
* **Records Returned:** 20
* **Execution Status:** Success

---

## Explain / Query Plan
```json
{
  "stage": "LIMIT",
  "inputStage": {
    "stage": "FETCH",
    "inputStage": {
      "stage": "IXSCAN",
      "indexName": "customer_id_1_created_at_-1_status_1",
      "keysExamined": 20,
      "docsExamined": 20
    }
  }
}
```

---

## Measurements
* **Execution Time:** 1.84 ms
* **Keys Examined:** 20
* **Docs Examined:** 20
* **Data Transferred:** 4.2 KB

---

## Edge Cases
1. **Brand New Customer:** Returns empty array in 0.4ms without disk I/O.
2. **Wholesale Customer (Hotspot):** Customer with 50,000 orders. Because index is sorted by `created_at DESC`, `limit(20)` still halts scan after reading only 20 keys.

---

## Scale Concerns
* If a customer has millions of orders, embedding items within the single document will cause document size limit violations (16MB BSON limit). That is why items are bounded or modeled in separate partitions.

---

## Alternative Model
* **Wide-Column (Cassandra):** Table `orders_by_customer` with `PRIMARY KEY ((customer_id), created_at, order_id) WITH CLUSTERING ORDER BY (created_at DESC)`.
* Advantage: Physical layout on disk is pre-sorted sequentially.

---

## Alternative Database
* **DynamoDB:** PK=`CUSTOMER#CUST-1049`, SK=`ORDER#2026-09-25#ORD-9481`.
* Query via `KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)"`.

---

## SQL Comparison
```sql
SELECT order_id, created_at, total_amount, json_array_length(items)
FROM orders
WHERE customer_id = 'CUST-1049' AND status = 'CONFIRMED'
ORDER BY created_at DESC
LIMIT 20;
```
* **Comparison:** SQL planner requires index on `(customer_id, created_at DESC)` to avoid a sort buffer (`Using filesort`). The document model delivers equivalent speed if indexed properly, but avoids joining an order items table.

---

## Explanation
The query achieves O(log N + K) targeted execution because the partition key isolates the query to a single shard, and the compound index matches the Equality-Sort-Range (ESR) rule.
