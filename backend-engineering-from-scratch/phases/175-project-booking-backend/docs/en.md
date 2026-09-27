# Lesson 175: Project: Booking Backend

> **Motto**: Build a high-concurrency reservation engine managing time slots, temporary holds, expiration timers, and double-booking defense.

---

## Motto
"Build a high-concurrency reservation engine managing time slots, temporary holds, expiration timers, and double-booking defense."

## Problem
Allowing two customers to book the same doctor appointment or hotel room destroys business reputation and customer trust.

## Prediction
Implementing temporary holds with TTL expiration, state machine transitions, and database exclusion constraints prevents double booking.

## Why this matters
Booking engines are the gold standard for testing complex temporal business rules and high-contention concurrency.

## First principles
Hold Slot (10-minute TTL) -> Customer Pays -> Confirm Booking. If TTL expires without payment -> Release Slot.

## Mental model
```text
Slot: AVAILABLE ──[Hold (10m TTL)]──> HELD ──┬──[Payment Succeeded]──> BOOKED (Permanent)
                                              └──[TTL Expires]─────────> AVAILABLE (Released)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Time-slot reservation and booking state machine implementation.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/175-project-booking-backend/tests/ -v
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
- **Failure Injection**: Two concurrent clients attempt to reserve the same time slot at the exact same millisecond.
- Execute the experiment script:
```bash
python phases/175-project-booking-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: First client acquires hold; second client receives HTTP 409 Conflict; held slot automatically expires after TTL if unpaid.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use PostgreSQL exclusion constraints (`EXCLUDE USING gist`) to prevent overlapping time ranges mathematically.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Run a periodic background sweeper or Redis keyspace expiration listener to release expired holds automatically.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Separate the concept of a temporary 'Hold' from a permanent 'Booking' in the domain model.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How do temporary slot holds with TTL expiration prevent inventory hoarding while customers enter payment details?
2. What database constraints or locking mechanisms prevent two users from booking the exact same time slot concurrently?
3. How does the booking state machine handle a payment confirmation webhook arriving after the hold timer expired?

## What comes next
Having understood project: booking backend, we next discover its inherent boundaries and transition to **Project: Notification Service**.
