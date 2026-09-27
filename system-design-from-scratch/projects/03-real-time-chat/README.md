# Capstone 03: Real-Time Chat Platform

> **Overview**: WebSocket connection manager, room Pub/Sub broadcasting, user presence tracking, and message history.

---

## 1. System Architecture
This production capstone implements a resilient distributed subsystem adhering to first principles:
- Measured single-node baseline evolved under simulated scale pressure.
- Clean separation of concerns between API gateway, persistence, and async workers.
- Resilience mechanisms protecting downstream dependencies under failure.

## 2. Verification Test Suite
Execute the project test suite:
```bash
pytest projects/03-real-time-chat/tests/ -v
```
