# Project: Webhook Delivery Platform

> **Overview**: Outbound webhook delivery with HMAC-SHA256 signatures, retry schedules, and DLQ isolation.

---

## 1. System Architecture
This standalone project implements a production-grade backend service adhering to first-principles design:
- Clean modular layer separation
- Defensive bounds and explicit error handling
- Concurrency and transaction safety

## 2. API & Data Contract
Refer to `app/main.py` for entity models, data transfer objects (DTOs), and core service interfaces.

## 3. Running and Testing
Execute the project test suite:
```bash
pytest projects/09-webhook-delivery-platform/tests/ -v
```
