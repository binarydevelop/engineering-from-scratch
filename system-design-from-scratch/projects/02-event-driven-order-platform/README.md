# Capstone 02: Event-Driven Order Platform

> **Overview**: Transactional Outbox pattern coordinating order commits, inventory deduction, and asynchronous event worker dispatch.

---

## 1. System Architecture
This production capstone implements a resilient distributed subsystem adhering to first principles:
- Measured single-node baseline evolved under simulated scale pressure.
- Clean separation of concerns between API gateway, persistence, and async workers.
- Resilience mechanisms protecting downstream dependencies under failure.

## 2. Verification Test Suite
Execute the project test suite:
```bash
pytest projects/02-event-driven-order-platform/tests/ -v
```
