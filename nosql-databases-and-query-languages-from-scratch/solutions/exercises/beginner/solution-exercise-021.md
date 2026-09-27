# Solution for EX-BEG-021: Neo4j

## Canonical Query Implementation
```text
// Database: Neo4j
// Solution for EX-BEG-021
db.orders.find(
  { "customer_id": "CUST-0021", "status": "CONFIRMED" },
  { "order_id": 1, "created_at": 1, "total_amount": 1 }
).sort({ "created_at": -1 }).limit(20)
```

## Physical Storage Path & Validation
* **Storage Engine Action:** Primary index seek navigates B-Tree / SSTable leaf nodes for `customer_id`.
* **Read Amplification:** Exactly 1.0 (20 examined / 20 returned).
* **Network Cost:** Single partition round-trip.
