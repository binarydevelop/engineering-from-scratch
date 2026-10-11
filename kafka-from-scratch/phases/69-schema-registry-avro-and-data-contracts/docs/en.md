# Phase 69: Schema Registry, Avro Serialization, and Event Data Contracts

## 1. Why This Matters for MAANG & Senior/Staff Roles
In an event-driven microservices architecture, messages sent over Kafka represent the public API contract between teams. Sending raw JSON without schema validation leads to catastrophic downstream runtime breakages when producer teams rename fields or change types. Schema Registry enforces centralized, versioned data contracts with compile-time and runtime compatibility checks.

---

## 2. Core Concepts & Architecture Deep-Dive
### Serialization Formats & Wire Overhead
- **JSON Overhead**: Includes schema keys in every message payload, increasing bandwidth and storage by 3x-5x. Lacks schema validation.
- **Apache Avro**: Binary serialization format where data is serialized against a schema. Payloads contain only compact binary data preceded by a 5-byte header (magic byte + 4-byte Schema ID registered in Schema Registry). Consumers fetch the schema by ID and deserialize safely.

### Schema Compatibility Modes
1. **BACKWARD (Default)**: Consumers with the new schema can read messages written with the previous schema. Rule: only delete optional fields or add optional fields with defaults.
2. **FORWARD**: Consumers with the old schema can read messages written with the new schema. Rule: only add new fields or delete optional fields.
3. **FULL**: Backward and Forward compatible simultaneously. Safe for rolling upgrades in any order.
4. **NONE**: Disables validation (dangerous in production).

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Design Scenarios
- **"How do you execute zero-downtime upgrades of event schemas across 50 consumer teams?"**:
  Enforce `FULL` compatibility mode in Schema Registry. Add new fields with default values. Deploy all consumers first, verify backward compatibility, then deploy updated producers.
- **"Why does Schema Registry use a 5-byte header in Kafka payloads?"**:
  Byte 0: Magic byte (0x0). Bytes 1-4: 32-bit Big-Endian Schema ID. Avoids transmitting full JSON schema with every record while ensuring exact deserialization schema lookup.

---

## 4. Hands-On Practice & Implementation Drills
### Avro Schema Definition Pattern
```json
{
  "type": "record",
  "name": "OrderPlacedEvent",
  "namespace": "com.company.orders",
  "doc": "Event emitted when a customer successfully places an order",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "customerId", "type": "string" },
    { "name": "totalAmount", "type": "bytes", "logicalType": "decimal", "precision": 10, "scale": 2 },
    { "name": "status", "type": { "type": "enum", "name": "OrderStatus", "symbols": ["PENDING", "CONFIRMED"] } },
    { "name": "discountCode", "type": ["null", "string"], "default": null },
    { "name": "createdAtEpochMs", "type": "long" }
  ]
}
```

---

## 5. Key Takeaways & Cheat Sheet
- Schema Registry enforces strict data contracts on Kafka topics.
- Avro strips field names from messages, reducing payload size drastically.
- Use FULL or BACKWARD compatibility modes to guarantee safe rolling upgrades.
- Eliminates downstream deserialization crashes across organizational boundaries.
