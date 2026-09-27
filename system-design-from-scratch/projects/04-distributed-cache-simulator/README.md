# Capstone 04: Distributed Cache Simulator

> **Overview**: Distributed cache cluster with consistent hash ring, virtual nodes, primary-replica replication, and node failover.

---

## 1. System Architecture
This production capstone implements a resilient distributed subsystem adhering to first principles:
- Measured single-node baseline evolved under simulated scale pressure.
- Clean separation of concerns between API gateway, persistence, and async workers.
- Resilience mechanisms protecting downstream dependencies under failure.

## 2. Verification Test Suite
Execute the project test suite:
```bash
pytest projects/04-distributed-cache-simulator/tests/ -v
```
