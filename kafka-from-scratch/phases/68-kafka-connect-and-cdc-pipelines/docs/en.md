# Phase 68: Kafka Connect Framework, Debezium, and Production CDC Architecture

## 1. Why This Matters for MAANG & Senior/Staff Roles
Writing custom applications to ingest data from relational databases into Kafka or stream data from Kafka into data warehouses/search engines is an anti-pattern. Kafka Connect is a battle-tested, fault-tolerant distributed runtime designed specifically to move massive data streams into and out of Apache Kafka with exactly-once or at-least-once guarantees.

---

## 2. Core Concepts & Architecture Deep-Dive
### Kafka Connect Distributed Architecture
- **Connectors**: High-level coordinate logic (SourceConnector or SinkConnector).
- **Tasks**: Independent worker threads that execute data movement. A connector partitions its work into N tasks distributed across Connect cluster worker nodes.
- **Converters**: Pluggable serializers/deserializers (AvroConverter, JsonConverter, ProtobufConverter).
- **Single Message Transforms (SMTs)**: Lightweight, inline record modification (filtering, masking PII, routing) before writing to Kafka or external sinks.

### Change Data Capture (CDC) via Debezium
Debezium monitors database transaction logs (PostgreSQL WAL via `pgoutput`, MySQL binlog, MongoDB oplog) and emits row-level change events (`CREATE`, `UPDATE`, `DELETE`) with before/after state:
- Captures 100% of mutations, including those bypassed by application-level events.
- Zero dual-write risk: database write is the single source of truth; CDC streams it to Kafka asynchronously.

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Failure Modes
- **"How do you keep Elasticsearch or read caches in sync with PostgreSQL without dual-writes?"**:
  Write to PostgreSQL -> Debezium reads WAL -> publishes change events to Kafka -> Kafka Connect Elasticsearch Sink writes to ES. Eliminates network split failures and race conditions inherent in manual dual writes.
- **"What happens during database schema migrations (ALTER TABLE)?"**:
  Schema evolution must be configured. Debezium parses DDL changes and updates Schema Registry. If incompatible, Connect can pause the connector or route poison pills to a Dead Letter Queue (DLQ).

---

## 4. Hands-On Practice & Implementation Drills
### Connector Configuration Pattern
```json
{
  "name": "postgres-order-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "pg-primary.internal",
    "database.port": "5432",
    "database.user": "cdc_user",
    "database.dbname": "orders_db",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
  }
}
```

---

## 5. Key Takeaways & Cheat Sheet
- Kafka Connect standardizes source and sink integration without writing bespoke code.
- Debezium tailing DB transaction logs eliminates dual-write consistency hazards.
- Connect clusters scale and rebalance tasks automatically upon worker failure.
- Core building block for real-time data pipelines and search index synchronization.
