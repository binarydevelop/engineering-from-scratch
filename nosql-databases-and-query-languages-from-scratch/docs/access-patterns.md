# Access Pattern Catalog & Query-First Modeling

In relational databases, schema design begins with conceptual entity-relationship modeling (ER diagrams, 3rd Normal Form). In NoSQL database engineering, schema design **begins with the access patterns**.

```text
Relational:  Entities & Relationships ──> Normalized Tables ──> Write Queries & Add Indexes
NoSQL:       Business Requirements ──> Access Patterns ──> Key & Partition Design ──> Data Model
```

---

## 1. Access Pattern Formal Specification

Every access pattern in a system must be cataloged using this standard specification:

| Field | Description | Example |
| :--- | :--- | :--- |
| **Pattern ID** | Unique identifier | `AP-ECOM-03` |
| **Name** | Descriptive action | Fetch order history for customer |
| **Actor** | Calling client / service | Mobile Client Order History Screen |
| **Frequency** | Expected throughput | 1,200 reads/sec (p99 < 15ms) |
| **Known Parameters** | Keys available at request time | `customer_id`, `start_date`, `limit` |
| **Filter Conditions** | Predicates applied | `status != 'CANCELLED'` |
| **Ordering** | Physical sort requirement | `order_timestamp DESC` |
| **Volume / Cardinality** | Target data size | 10–50 orders per customer; top 0.1% has 5,000 |
| **Consistency SLA** | Required staleness bound | Eventual consistency acceptable (< 1 sec lag) |

---

## 2. Common Cross-Industry Access Patterns

### A. E-Commerce Domain
* **`AP-ECOM-01` (Point Lookup):** Get product details by SKU / Product ID.
  - *Parameters:* `product_id`
  - *SLA:* 15,000 QPS, p99 < 3ms
  - *Ideal Models:* Key-Value (Redis `GET`), Document (Mongo `_id`), DynamoDB (`PK=PRODUCT#<id>`)
* **`AP-ECOM-02` (Customer Order Stream):** List recent orders for customer with status.
  - *Parameters:* `customer_id`, limit 20
  - *SLA:* 2,500 QPS, p99 < 10ms
  - *Ideal Models:* Cassandra (`PRIMARY KEY ((customer_id), created_at DESC)`), DynamoDB (`PK=CUST#id`, `SK begins_with("ORD#")`)
* **`AP-ECOM-03` (Catalog Discovery & Filtering):** Search products by keyword, category, price range, and brand with faceted counts.
  - *Parameters:* `query_text`, `category_id`, `price_min`, `price_max`
  - *Ideal Models:* Inverted Index (Elasticsearch `bool` query with `must` match + `filter` range + `terms` aggregations)
* **`AP-ECOM-04` (Shopping Cart Mutation):** Atomically add, remove, or update quantity of SKU in user session.
  - *Parameters:* `session_id`, `sku_id`, `delta_qty`
  - *Ideal Models:* Document (Mongo `$inc`, `$push` to array), Redis Hash (`HINCRBY`)

### B. Social Networking Domain
* **`AP-SOC-01` (Timeline / Feed Generation):** Retrieve the latest 50 posts from followed users.
  - *Fan-out on Read:* Query wide-column table for all followed users and merge-sort (high read cost).
  - *Fan-out on Write:* Push new post ID into pre-computed Redis/Cassandra inbox of all followers (high write cost).
* **`AP-SOC-02` (Friend-of-Friend Recommendations):** Find mutual connections between user A and user B.
  - *Ideal Model:* Property Graph (Neo4j Cypher `MATCH (a:User)-[:FRIEND]->(f)-[:FRIEND]->(b)`).

### C. IoT & Telemetry Domain
* **`AP-IOT-01` (Time-Series Metric Ingest):** Ingest 500,000 sensor readings/sec with device timestamp and telemetry payload.
  - *Ideal Model:* Wide-Column LSM Tree (Cassandra / ScyllaDB) with `PRIMARY KEY ((device_id, date), timestamp)` to bound partition size to a single day.
* **`AP-IOT-02` (Latest Device Status):** Return the most recent telemetry ping for a fleet of 100,000 devices.
  - *Ideal Model:* Redis Hash or Document key lookup.

### D. SaaS & Multi-Tenancy Domain
* **`AP-SAAS-01` (Tenant Data Isolation):** Ensure all tenant queries are physically isolated to tenant partitions.
  - *Partition Key:* `tenant_id` (Ensures zero cross-tenant data leakage and fast sharded queries).
* **`AP-SAAS-02` (Audit Trail Exploration):** Filter enterprise audit logs by user, date range, action type, and IP address.
  - *Ideal Model:* Elasticsearch / OpenSearch structured log index with daily time-based indices.

---

## 3. The Query-First Checklist

Before approving any data schema, answer these four verification questions:

1. **Does the schema allow every high-frequency access pattern to target a single partition key?**
2. **Are sorting requirements satisfied by physical clustering column order rather than in-memory sort buffers?**
3. **Is bounded data embedded within document aggregates, while unbounded data is referenced or split across partitions?**
4. **Is every cross-entity join required by the UI either eliminated through intentional denormalization or shifted to an asynchronous search projection?**
