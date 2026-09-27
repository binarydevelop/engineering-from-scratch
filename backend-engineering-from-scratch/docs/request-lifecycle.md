# The Complete End-to-End Request Lifecycle: Tracing `POST /orders`

To master backend engineering, an engineer must be able to trace a realistic state-modifying mutation from physical network wire frames to persistent disk blocks and asynchronous event queues.

```http
POST /orders HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
Idempotency-Key: 7b9d3e82-411a-4c2f-b4e8-89fae1d93b12
Content-Type: application/json
Content-Length: 142

{
  "tenant_id": "tenant_abc",
  "items": [
    {"product_id": "prod_101", "quantity": 2}
  ]
}
```

---

## The 12 Stages of Request Traversal

```text
[1. Client & DNS Resolution]
            │
            ▼
[2. Transport Layer: TCP 3-Way Handshake + TLS 1.3]
            │
            ▼
[3. Reverse Proxy / Ingress Load Balancer]
            │
            ▼
[4. ASGI Web Server & Protocol Parser]
            │
            ▼
[5. Outer Middleware Pipeline: Correlation ID & Logging]
            │
            ▼
[6. Security & Authentication Boundary]
            │
            ▼
[7. URL Routing & Strict Schema Validation]
            │
            ▼
[8. Application / Use-Case Service & Idempotency Check]
            │
            ▼
[9. Domain Logic & Invariants Enforcement]
            │
            ▼
[10. Database Persistence & Transaction Boundary]
            │
            ▼
[11. Cache Invalidation & Asynchronous Outbox Relay]
            │
            ▼
[12. Response Serialization & Socket Return]
```

---

## Detailed Layer Breakdown Matrix

| Layer | Responsibility | What Can Fail? | Retry Policy | Transactional? | Async vs Sync | Concurrency Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. DNS & Network** | Resolves domain name to IP; establishes routing across Internet routers. | NXDOMAIN, DNS timeout, packet loss, BGP blackhole. | **Safe to retry** at transport layer (SYN retransmissions). | No | Sync | None |
| **2. TLS & TCP Handshake** | Establishes cryptographic session, negotiates cipher, sets up receive/send buffers. | Expired certificate, cipher mismatch, TCP connection refused (port backlog full). | **Safe to retry** with exponential backoff if connect fails. | No | Sync | Ephemeral port exhaustion under high connection churn. |
| **3. Reverse Proxy (Nginx/ALB)** | Terminates TLS, buffers slow clients, enforces DDoS protections, load balances. | Upstream connection timeout (504), all backends saturated (502/503). | **Do NOT retry POST blindly** without idempotency key. | No | Sync | Proxy worker file descriptor limits. |
| **4. Web Server (ASGI/Uvicorn)** | Reads bytes from OS socket buffer, parses HTTP/1.1 or HTTP/2 headers into Python scope. | Truncated request body, malformed header, connection reset by peer. | Client may retry if socket resets before headers parsed. | No | Sync | Worker process thread saturation. |
| **5. Middleware Pipeline** | Generates `X-Request-ID`, starts latency timer, enforces rate limit per IP/user. | Rate limit exceeded (429 Too Many Requests), malformed correlation headers. | Client should back off and respect `Retry-After` header. | No | Sync | In-memory rate limiter can race if not using atomic Redis script. |
| **6. Authentication (AuthN)** | Validates bearer token signature, checks token expiration, resolves principal identity. | Invalid signature (401 Unauthorized), expired token, tampered claims. | **Do NOT retry** until client acquires refreshed token. | No | Sync | Key rotation race if public key cache is not synchronized. |
| **7. Routing & Validation** | Matches `POST /orders`, parses JSON, verifies required fields, types, and constraints. | Malformed JSON syntax (400), schema validation failure (422 Unprocessable Entity). | **Do NOT retry**; payload must be corrected by client. | No | Sync | None |
| **8. Use-Case & Idempotency** | Checks if `Idempotency-Key` was already executed; verifies authorization for tenant. | Unauthorized tenant access (403 Forbidden), concurrent duplicate request in flight (409 Conflict). | If cached response exists, return previous result immediately without re-execution. | Lookup should be fast (Redis or SQL). | Sync | **Critical race**: Two simultaneous requests with same key must not both execute. |
| **9. Domain Invariants** | Evaluates business rules: is store open? is account active? are items valid? | Invariant violation (e.g. minimum order value not met, product discontinued). | **Do NOT retry** without modifying business parameters. | Must hold inside transaction. | Sync | Stale state read if checked outside lock. |
| **10. Database Transaction** | Atomic multi-row update: locks inventory (`SELECT FOR UPDATE`), decrements stock, inserts order and outbox record. | Deadlock detected (40001), check constraint violation (insufficient stock), DB connection timeout. | **Deadlock: Safe to retry** the transaction internally with backoff. **Constraint: Do NOT retry**. | **MANDATORY ACID TRANSACTION** | Sync | **High race**: Multiple users competing for the last inventory item. Row-level locks prevent overselling. |
| **11. Cache & Outbox Relay** | Invalidates stale catalog cache; background worker reads committed outbox event and publishes to broker. | Redis cache node unreachable; message broker temporarily down. | **Fail-open for cache** (log warning). **Outbox relay retries infinitely** with backoff until broker ACKs. | Invalidation is post-commit; outbox record insertion is inside transaction. | **Asynchronous for broker publish & email** | Cache stampede if hot key expires while invalidating. |
| **12. Response Serialization** | Converts domain order object into API response DTO, writes HTTP 201 Created with JSON and headers. | Serialization error (unexpected circular reference or unhandled type), socket broken pipe. | Client receives 201. If client socket dropped before receiving, client retries with Idempotency-Key. | No | Sync | Memory allocation for massive response payloads. |

---

## What Must Never Be Done Synchronously in `POST /orders`
1. **Never send transactional emails in the HTTP request loop**: If SendGrid or SMTP takes 4.5 seconds to reply or hangs, your API latency skyrockets to 4.5 seconds, locking a web worker and connection.
2. **Never call payment gateways without an explicit timeout and idempotency key**: If Stripe or PayPal times out at 30 seconds, your system must know whether the charge went through before blindly retrying.
3. **Never publish directly to an external message queue without an outbox**: If the message queue publish succeeds but your PostgreSQL commit fails due to a constraint, you have published a phantom event that will confuse downstream warehouse services.
