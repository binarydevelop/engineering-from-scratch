# Capstone 06: Tiny Distributed KV Store

> **Overview**: Leaderless key-value store with configurable N/W/R quorums and hinted handoff replication.

---

## 1. System Architecture
This production capstone implements a resilient distributed subsystem adhering to first principles:
- Measured single-node baseline evolved under simulated scale pressure.
- Clean separation of concerns between API gateway, persistence, and async workers.
- Resilience mechanisms protecting downstream dependencies under failure.

## 2. Verification Test Suite
Execute the project test suite:
```bash
pytest projects/06-tiny-distributed-kv-store/tests/ -v
```
