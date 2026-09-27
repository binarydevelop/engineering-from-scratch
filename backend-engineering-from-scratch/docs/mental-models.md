# Foundational Backend Mental Models

To design robust distributed backend systems, an engineer must replace vague intuitive metaphors with precise physical and operational mental models.

---

## 1. The Onion Model of HTTP Request Execution

Every web framework request travels inward through nested layers of context and then bubbles outward:

```text
Incoming Raw TCP Bytes
        │
        ▼
┌────────────────────────────────────────────────────────┐
│ 1. Network & Protocol Layer (Socket / TLS / HTTP Parser)│
│    Bytes -> RFC 9112 Framing -> Request Object         │
│    ┌──────────────────────────────────────────────────┐│
│    │ 2. Outer Middleware (Request ID, Logging, CORS)  ││
│    │    ┌────────────────────────────────────────────┐││
│    │    │ 3. Security Boundary (AuthN, Rate Limit)   │││
│    │    │    ┌──────────────────────────────────────┐│││
│    │    │    │ 4. Router & Validation (Path, Schema)││││
│    │    │    │    ┌────────────────────────────────┐││││
│    │    │    │    │ 5. Application / Use-Case Logic│││││
│    │    │    │    │    ┌──────────────────────────┐│││││
│    │    │    │    │    │ 6. Domain Core & Business││││││
│    │    │    │    │    │    Rules Invariants      ││││││
│    │    │    │    │    └─────────────┬────────────┘│││││
│    │    │    │    │ 7. Persistence & External APIs │││││
│    │    │    │    │    (SQL Transaction / Redis)   │││││
│    │    │    │    └─────────────┬──────────────────┘││││
│    │    │    │ Response Serialization (JSON/Headers)││││
│    │    │    └──────────────────┬───────────────────┘│││
│    │    │ AuthZ & Audit Logging ┴                    │││
│    │    └───────────────────────┬────────────────────┘││
│    │ Latency Measurement & Access Log Emitted        ││
│    └────────────────────────────┬─────────────────────┘│
│ Outgoing HTTP Response Bytes (Status Line + Headers + Body)
└─────────────────────────────────┬──────────────────────┘
                                  ▼
                        Socket Write to Client
```

---

## 2. Little's Law and Server Capacity

A backend server does not have an infinite ability to hold requests in flight. Little's Law states:

$$L = \lambda \times W$$

Where:
- $L$ = Number of concurrent requests inside the system (concurrency in flight)
- $\lambda$ = Arrival rate of requests (Requests Per Second / RPS)
- $W$ = Average time a request spends in the system (Latency in seconds)

### The Capacity Trap
If your service handles $1,000\text{ RPS}$ and average latency is $50\text{ ms}\ (0.05\text{ s})$:
$$L = 1000 \times 0.05 = 50\text{ concurrent requests}$$

Now suppose a downstream database slows down due to lock contention or a missing index, causing latency to increase to $2.0\text{ seconds}$:
$$L = 1000 \times 2.0 = 2,000\text{ concurrent requests}$$

If your worker pool or connection pool only has capacity for 200 concurrent tasks:
- All 200 workers become saturated waiting for the slow queries
- Sockets buffer requests until operating system TCP backlogs fill
- Reverse proxies encounter connection timeouts and return HTTP 504
- Memory explodes and the process crashes due to OOM

**Key Takeaway**: Latency spikes directly multiply concurrency demand. Performance is not just about speed; it is about survival under concurrency.

---

## 3. The Dual-Write Problem

A common amateur backend pattern:

```python
# ANTI-PATTERN: Dual Write
db.commit_order(order)       # Step 1: Database Write
kafka.publish("order_placed") # Step 2: External Broker Call
```

### The Inherent Flaw
Step 1 and Step 2 run across distinct network boundaries. There is no distributed consensus across a standard SQL database and an external message queue without two-phase commit:
1. If Step 1 succeeds and the process crashes before Step 2, the order exists but the event is never published. Inventory is not reserved, emails are not sent.
2. If we reverse the order and publish the message first, and then the database transaction rolls back due to a constraint violation, external systems react to an order that does not exist in the database!

### The Solution: Transactional Outbox
```text
┌──────────────────────────────────────────────┐
│ Single Atomic SQL Transaction (ACID)         │
│                                              │
│ 1. INSERT INTO orders (...)                  │
│ 2. INSERT INTO outbox_events (event, status) │
│                                              │
│ COMMIT                                       │
└───────────────────────┬──────────────────────┘
                        │
                        ▼ (Asynchronous Relay)
┌──────────────────────────────────────────────┐
│ Outbox Poller / Dequeue Worker               │
│ Reads outbox_events -> Publishes to Broker   │
│ Marks event as published upon ACK            │
└──────────────────────────────────────────────┘
```
The transactional outbox guarantees **at-least-once** event publishing without dual-write failure.
