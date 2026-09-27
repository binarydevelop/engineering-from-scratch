# Capstone 07: Production-Like Social Feed

> **Overview**: Activity feed generation platform implementing hybrid fanout handling both regular users and hot celebrity accounts.

---

## 1. System Architecture
This production capstone implements a resilient distributed subsystem adhering to first principles:
- Measured single-node baseline evolved under simulated scale pressure.
- Clean separation of concerns between API gateway, persistence, and async workers.
- Resilience mechanisms protecting downstream dependencies under failure.

## 2. Verification Test Suite
Execute the project test suite:
```bash
pytest projects/07-production-social-feed/tests/ -v
```
