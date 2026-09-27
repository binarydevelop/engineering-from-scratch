# Backend Production Readiness Review Checklist

Before releasing any backend service into production, evaluate each item. A single unchecked item can cause an outage or compromise system integrity under load.

---

## 1. Network & Protocol Layer
- [ ] **TLS Termination**: Enforce TLS 1.3/1.2; disable obsolete SSL ciphers; redirect HTTP to HTTPS.
- [ ] **Reverse Proxy Limits**: Nginx/Caddy configured with `client_max_body_size` (e.g. 10MB) to reject huge payload denial-of-service attacks.
- [ ] **TCP Backlog**: OS `net.core.somaxconn` tuned appropriately for expected socket concurrency.
- [ ] **CORS Configuration**: Explicit origin whitelist configured; no wildcards (`*`) with credentials enabled.

## 2. Process & Runtime Management
- [ ] **Graceful Shutdown**: Service listens for `SIGTERM` / `SIGINT`; immediately stops accepting new requests; allows in-flight requests 15–30 seconds to finish; safely closes DB pools and worker connections.
- [ ] **Stateless Replicas**: No state stored in local process memory (sessions, caches, file uploads); all replicas share external stores (Redis, S3, SQL).
- [ ] **Non-Root Container**: Docker container runs under an unprivileged user (`USER appuser`).
- [ ] **Resource Limits**: CPU requests/limits and memory limits explicitly set in container manifests to prevent node starvation.

## 3. Database & Persistence Layer
- [ ] **Bounded Connection Pool**: Connection pool `min_size` and `max_size` explicitly configured. Pool max size should never exceed total allowed database connections across all replicas:
  $$\text{Total Connections} = \text{Replicas} \times \text{Pool Size} < \text{max\_connections} - \text{buffer}$$
- [ ] **Connection Timeouts**: Pool acquisition timeout configured (e.g. 5.0s) so requests fail fast rather than hanging indefinitely.
- [ ] **Statement Timeouts**: Database statement timeout configured (e.g. 10s) to prevent runaway runaway queries from locking tables.
- [ ] **All Foreign Keys & Search Fields Indexed**: Foreign keys have supporting B-Tree indexes; query performance verified with `EXPLAIN ANALYZE`.
- [ ] **Safe Schema Migrations**: Zero-downtime migration strategy followed (expand, backfill, contract). No lock-heavy instant column drops or renames on hot production tables.

## 4. Resilience & Dependency Defense
- [ ] **Outbound Network Timeouts**: Every external HTTP/TCP call has an explicit connect timeout (<= 2s) and read timeout (<= 10s).
- [ ] **Retries with Exponential Backoff & Jitter**: Retries restricted strictly to idempotent operations; max retry count capped (e.g. 3 attempts); jitter added to prevent thundering herds.
- [ ] **Circuit Breakers**: Circuit breaker installed on non-critical downstream dependencies to fail fast when services degrade.
- [ ] **Bulkheads & Concurrency Limits**: Separate connection pools or rate limits for independent third-party integrations.

## 5. Security & Access Control
- [ ] **Parameterized SQL Only**: Zero string formatting or concatenation in database queries.
- [ ] **Work-Factor Password Hashing**: Passwords hashed using `bcrypt` or `Argon2id`; work factor tuned to >= 12.
- [ ] **Token Expiration & Signature Enforcement**: JWT tokens signed cryptographically with expiration enforced; `none` algorithm rejected.
- [ ] **Object-Level Authorization**: Enforce tenant and user resource ownership on every query (`WHERE tenant_id = :tenant_id AND id = :id`).
- [ ] **Rate Limiting**: Authentication, password reset, and public endpoints throttled by IP and user identity.
- [ ] **Secret Hygiene**: Zero hardcoded secrets; injected via environment variables or secret manager; `.env` excluded from version control.

## 6. Observability & Telemetry
- [ ] **Health Checks**: `/health/live` (process alive) and `/health/ready` (DB pool connected and ready) endpoints exposed without expensive queries.
- [ ] **Correlation IDs**: `X-Request-ID` generated at ingress, propagated through ASGI scope, database comments, and worker queues.
- [ ] **Structured JSON Logs**: Logs output as structured JSON containing timestamp, severity level, request ID, user ID, and execution duration.
- [ ] **No Sensitive Data in Logs**: Passwords, tokens, credit card numbers, and PII strictly redacted from logging pipelines.
- [ ] **RED Metrics Instrumented**: Prometheus / OpenTelemetry metrics for Rate (RPS), Errors (4xx/5xx counts), and Duration (p50, p95, p99 latency histograms).

## 7. Asynchronous & Background Work
- [ ] **Bounded Queues**: Queues have maximum depth limits; reject or shed load when queue depth explodes.
- [ ] **Idempotent Workers**: Every background task can be executed twice without corrupting state or creating duplicate side effects.
- [ ] **Dead-Letter Queue (DLQ)**: Tasks that fail after max retries are moved to a DLQ with operational alerting.
- [ ] **Transactional Outbox**: Events emitted from database state changes are saved in the same local transaction to eliminate dual-write inconsistencies.
