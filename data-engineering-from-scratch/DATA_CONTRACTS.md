# Data Contracts: Producer-Consumer Specification Framework

> **Motto**: A data pipeline without a contract is an unhandled breaking change waiting to happen.

---

## 1. What Is a Data Contract?

A **Data Contract** is a formal, versioned agreement between a data producer (such as a backend service or ingestion pipeline) and downstream data consumers (analytics engineers, ML engineers, business analysts).

It defines:
1. **Schema**: Explicit field names, types, nullability, constraints, and defaults.
2. **Semantics**: Clear business definitions of fields and units of measurement.
3. **Freshness & Availability (SLAs/SLOs)**: Delivery frequency, expected arrival times, and maximum tolerable lag.
4. **Ownership & Governance**: The producing team, primary point of contact, classification (PII, financial), and access policies.
5. **Quality Constraints**: Minimum row volumes, allowed value sets, range bounds, and referential integrity.
6. **Evolution Rules**: Strict policies governing backward and forward compatibility.

---

## 2. The Core Problem: Silent Data Corruption

In traditional architectures, application databases are treated as internal implementation details, yet downstream data teams query replicas or dump tables directly.
When a backend software engineer renames a column from `user_id` to `customer_uuid`, or changes a timestamp from UTC to epoch milliseconds, downstream systems fail silently:
- The nightly ETL job completes successfully.
- Dashboards report zero revenue or missing users.
- Machine learning models degrade silently because features drift.

A data contract decouples internal application persistence from the authoritative analytical interface.

---

## 3. Reference Data Contract Specification (YAML Schema)

```yaml
version: "2.0.0"
contract_id: "contract.orders.events.v1"
dataset: "orders"
domain: "checkout"
owner:
  team: "orders-platform"
  slack_channel: "#team-checkout-data"
  oncall_pager: "pagerduty.com/services/PCHECKOUT"
classification: "CONFIDENTIAL" # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED

# Service Level Objectives
service_level_agreements:
  freshness:
    max_lag_minutes: 15
    schedule: "continuous-streaming"
  availability:
    uptime_percentage: 99.9
  data_retention:
    hot_storage_days: 90
    cold_archive_days: 2555 # 7 years financial compliance

# Schema Specification
schema:
  type: "record"
  name: "OrderEvent"
  fields:
    - name: "order_id"
      type: "string"
      nullable: false
      primary_key: true
      description: "Globally unique order identifier (UUIDv4 format)."
      example: "7b4c9e8a-40a2-4a0b-a63e-3cb0d201a4bc"

    - name: "customer_id"
      type: "string"
      nullable: false
      foreign_key: "contract.customers.v1.customer_id"
      description: "Identifier of the ordering customer."

    - name: "order_status"
      type: "string"
      nullable: false
      allowed_values: ["PENDING", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED", "REFUNDED"]
      description: "Lifecycle status of the order."

    - name: "currency"
      type: "string"
      nullable: false
      pattern: "^[A-Z]{3}$"
      description: "ISO 4217 three-letter currency code."
      example: "USD"

    - name: "subtotal_amount_cents"
      type: "integer"
      nullable: false
      minimum: 0
      description: "Total order price before tax and shipping, denominated in integer cents to avoid floating-point errors."

    - name: "tax_amount_cents"
      type: "integer"
      nullable: false
      minimum: 0
      description: "Tax applied to the order in integer cents."

    - name: "created_at"
      type: "timestamp_tz"
      nullable: false
      description: "ISO 8601 UTC timestamp when the order was initiated by customer."

    - name: "updated_at"
      type: "timestamp_tz"
      nullable: false
      description: "ISO 8601 UTC timestamp of last status change."

# Quality Invariants & Expectations
quality_rules:
  - id: "rule_positive_amount"
    description: "Subtotal amount must be greater than or equal to 0"
    assertion: "subtotal_amount_cents >= 0"
    severity: "CRITICAL" # CRITICAL rejects pipeline publish; WARNING alerts oncall

  - id: "rule_tax_proportion"
    description: "Tax cannot exceed 40% of subtotal under normal tax jurisdictions"
    assertion: "tax_amount_cents <= (subtotal_amount_cents * 0.40)"
    severity: "WARNING"

  - id: "rule_no_duplicate_orders"
    description: "order_id must be strictly unique within the delivery batch"
    assertion: "is_unique(order_id)"
    severity: "CRITICAL"

# Evolution Policy
evolution_rules:
  compatibility_mode: "BACKWARD"
  breaking_change_protocol:
    notice_period_days: 30
    dual_write_required: true
```

---

## 4. Producer vs Consumer Obligations

| Dimension | Producer Obligations | Consumer Obligations |
| :--- | :--- | :--- |
| **Schema Integrity** | Must never publish payloads missing non-nullable fields or altering data types without bumping major contract version. | Must design parsers to tolerate newly added optional fields (forward compatibility). |
| **Freshness** | Must emit events or complete batch extraction within agreed SLA latency bounds. | Must monitor upstream freshness alerts and avoid polling faster than agreed contract intervals. |
| **Quality** | Must validate payloads at the boundary before writing to shared storage/broker (contract pre-flight tests). | Must quarantine corrupt records into dead-letter storage rather than crashing whole pipeline. |
| **Breaking Changes** | Must maintain dual-publishing for the migration period (minimum 30 days) and provide migration guides. | Must migrate downstream readers to new contract version within the migration window. |

---

## 5. Schema Evolution Compatibility Rules

```text
Producer Contract v1.0.0
       │
       ▼
Is change BACKWARD compatible?
  ├── Adding an optional field with default value? ──> YES (Minor bump: v1.1.0)
  ├── Relaxing a constraint (e.g., nullable: false -> true)? ──> NO (Breaks consumer!)
  ├── Changing type (e.g., integer -> string)? ──> NO (Breaks arithmetic!)
  ├── Removing a field? ──> NO (Breaks downstream SELECT!)
  └── Renaming a field? ──> NO (Treated as drop + add!)
```

### The 4 Modes of Compatibility
1. **Backward Compatible**: Consumers on schema $N$ can read data generated by producer on schema $N+1$. (Add optional fields).
2. **Forward Compatible**: Consumers on schema $N+1$ can read data generated by producer on schema $N$. (Delete optional fields).
3. **Full Compatible**: Both backward and forward compatible.
4. **Breaking / None**: Requires new dataset name, version prefix (e.g., `orders_v2`), or migration period with dual writes.

---

## 6. How Contracts Are Enforced in Practice

Contracts are NOT purely documentation; they are executable gates:
1. **At Code Time**: Schema linting in CI/CD before deploying application or pipeline code.
2. **At Ingestion Time**: Ingestion gate (Pydantic / Avro serializer / JSON Schema) rejects non-compliant payloads.
3. **At Warehouse Boundary**: SQL tests verify uniqueness, referential integrity, and value invariants before atomic swap.
