# Capstone 2: Resilient Event-Driven Application

A multi-worker e-commerce event pipeline demonstrating loose coupling, independent consumer groups, transactional idempotency, and non-blocking retry routing.

---

## 1. Components

1. **Order API:** Emits `OrderPlaced` domain events with UUIDs.
2. **Payment Worker:** Group `payment-workers`. Executes charges against an SQLite idempotency store. Routes transient errors to `orders.RETRY`.
3. **Email Worker:** Group `email-workers`. Sends order confirmations.
4. **Analytics Worker:** Group `bi-analytics`. Continuously computes real-time revenue.

---

## 2. Running the Application

```bash
python3 projects/capstone-2-event-driven-app/run_app.py
```
