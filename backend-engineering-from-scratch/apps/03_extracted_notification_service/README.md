# Capstone 03: Extracted Notification Service

A standalone notification microservice extracted from Capstone 01's monolith.
Demonstrates decoupled asynchronous service boundaries:
- **Queue/Bus Ingestion**: Consumes domain events independently of the monolithic database.
- **Idempotent Processing**: Message deduplication store preventing duplicate notifications under at-least-once delivery.
- **Dead-Letter Queue (DLQ)**: Poison message isolation when downstream providers persistently fail.
- **HTTP and Queue Interfaces**: Decoupled network APIs.

---

## 1. Microservice Boundary

```text
Monolith Outbox Worker
        │
        ▼ (Publishes to Event Queue / HTTP POST)
[Extracted Notification Service]
        │
        ├──▶ Check Idempotency Store (Has this message ID been seen?)
        │       └── If YES: Acknowledge & skip execution (Deduplicated)
        │
        ├──▶ Outbound Delivery Adapter
        │       └── Try send notification (SES / SendGrid)
        │
        └── Failure after Max Retries?
                └── Route to Dead Letter Queue (DLQ)
```

## 2. Key Components
- `dedup.py`: In-memory / persistent deduplication lock.
- `delivery.py`: Multi-provider dispatch adapter.
- `consumer.py`: Event ingestion loop with exponential backoff and DLQ routing.

## 3. Running Tests
```bash
pytest apps/03_extracted_notification_service/tests/ -v
```
