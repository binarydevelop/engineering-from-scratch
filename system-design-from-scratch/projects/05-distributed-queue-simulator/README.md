# Capstone 05: Distributed Queue Simulator

> **Overview**: Partitioned message broker, consumer group offset management, visibility timeouts, and dead-letter queues.

---

## 1. System Architecture
This production capstone implements a resilient distributed subsystem adhering to first principles:
- Measured single-node baseline evolved under simulated scale pressure.
- Clean separation of concerns between API gateway, persistence, and async workers.
- Resilience mechanisms protecting downstream dependencies under failure.

## 2. Verification Test Suite
Execute the project test suite:
```bash
pytest projects/05-distributed-queue-simulator/tests/ -v
```
