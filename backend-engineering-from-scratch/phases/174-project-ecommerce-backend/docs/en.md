# Lesson 174: Project: E-Commerce Backend

> **Motto**: Build an e-commerce backend handling multi-table transactions, inventory reservation, row-level locking, and outbox events.

---

## Motto
"Build an e-commerce backend handling multi-table transactions, inventory reservation, row-level locking, and outbox events."

## Problem
Concurrently purchasing the last inventory item without row-level locking oversells stock, causing financial and logistical chaos.

## Prediction
Using `SELECT FOR UPDATE`, ACID transactions, and Transactional Outbox event publishing guarantees consistency under load.

## Why this matters
E-commerce backends represent the ultimate test of transaction boundaries, concurrency control, and distributed consistency.

## First principles
BEGIN -> Lock Stock (SELECT FOR UPDATE) -> Decrement Stock -> Insert Order -> Insert Outbox Event -> COMMIT.

## Mental model
```text
POST /orders -> SQL Tx: [Lock Inventory -> Decrement Stock -> Insert Order -> Insert Outbox] -> Commit -> 201 Created
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Production e-commerce transaction and inventory reservation service.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/174-project-ecommerce-backend/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Send 20 concurrent purchase requests for an item with stock = 1.
- Execute the experiment script:
```bash
python phases/174-project-ecommerce-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify exactly 1 purchase succeeds with HTTP 201; remaining 19 fail safely with HTTP 409 Conflict; final stock is exactly 0.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep checkout transactions as short as humanly possible: calculate prices and validate cards *before* locking inventory rows.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Publish `OrderPlaced` events via Transactional Outbox to trigger asynchronous email receipts and fulfillment.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Support idempotency keys on checkout endpoints to prevent double-charging clients who retry after network timeouts.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does `SELECT FOR UPDATE` prevent two concurrent users from simultaneously purchasing the last inventory item?
2. Why must inventory decrement, order creation, and outbox event insertion execute within the same ACID transaction?
3. What happens to inventory stock accuracy under concurrent traffic if row locking is omitted?

## What comes next
Having understood project: e-commerce backend, we next discover its inherent boundaries and transition to **Project: Booking Backend**.
