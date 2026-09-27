# Capstone 01: Modular Monolith

A production-grade Modular Monolith architecture in Python demonstrating:
- Strict domain module boundaries (`users`, `catalog`, `orders`, `notifications`)
- Shared database with transactional atomicity
- **Transactional Outbox Pattern** to reliably publish domain events without distributed 2PC transactions
- **RED Metrics** (Rate, Errors, Duration) and Request-ID tracing
- In-memory SQLite persistence compatible with PostgreSQL semantics

---

## 1. Architecture

```text
HTTP Request (POST /orders)
    │
    ▼ [Middleware: Request-ID + RED Metrics Timer]
[Orders Module]
    │──▶ Validate user & inventory (Catalog Module)
    │──▶ Open DB Transaction
    │       ├── Deduct Inventory
    │       ├── Insert Order Record
    │       └── Insert Outbox Event (Pending)
    └── Commit DB Transaction
            │
            ▼
[Notifications Module (Outbox Worker)]
    │──▶ Poll Outbox for pending events
    │──▶ Dispatch Notification (Email/SMS)
    └── Mark Outbox record as DISPATCHED
```

## 2. Modules
- **`users`**: Customer account credentials, identity, and profile storage.
- **`catalog`**: Product inventory stock management with pessimistic reservation checks.
- **`orders`**: Transactional order coordinator writing orders and outbox records in a single atomic transaction.
- **`notifications`**: Outbox consumer dispatching asynchronous domain notifications.
- **`observability`**: Structured logging, request-id propagation, and RED metrics counters.

## 3. Running Tests
```bash
pytest apps/01_modular_monolith/tests/ -v
```
