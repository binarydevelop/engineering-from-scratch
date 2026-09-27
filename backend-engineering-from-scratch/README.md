# backend-engineering-from-scratch

> **Understand it. Build it. Serve it. Persist it. Break it. Debug it. Secure it. Scale it. Operate it.**

---

[![Tests](https://img.shields.io/badge/tests-905%20passed-brightgreen.svg)](#test-suite-and-validation)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](VERSIONS.md)
[![Phases](https://img.shields.io/badge/phases-206%20complete-purple.svg)](ROADMAP.md)
[![Projects](https://img.shields.io/badge/projects-13%20services-orange.svg)](projects/)
[![Broken Labs](https://img.shields.io/badge/debugging%20labs-32%20solved-red.svg)](broken-systems/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

An exhaustive, first-principles curriculum designed to teach backend engineering deeply through implementation, empirical experiments, rigorous testing, measurement, failure injection, debugging, security auditing, and production operations.

Learners do not start by memorizing a web framework. Frameworks are introduced only after the underlying operating system and networking primitives—sockets, raw HTTP wire serialization, dispatch loops, and middleware chains—have been understood and built from scratch.

---

## The Target Mental Model

The learner should never think:
> *"Backend engineering means knowing FastAPI."*

The target mental model is:
> **Backend engineering is the discipline of designing reliable networked programs that accept requests, enforce business rules, manage state, coordinate external systems, survive failures, expose useful interfaces, and remain observable and operable in production.**

### Tracing a Request End-to-End

Every concept in this repository prepares you to trace a request like:
```http
POST /orders HTTP/1.1
Host: api.example.com
Authorization: Bearer <jwt-token>
Content-Type: application/json
Idempotency-Key: 7b8b2e3a-9c41-48e2

{"product_id": "prd_42", "quantity": 2}
```

through every single layer:

```text
client
  │
  ▼
DNS resolution / TCP handshake / TLS termination
  │
  ▼
BSD socket (accept, recv, non-blocking epoll/kqueue)
  │
  ▼
HTTP wire parser (method, path, headers, framing, chunked/content-length body)
  │
  ▼
Middleware onion pipeline (request-ID, RED metrics timer, rate limiting, panic recovery)
  │
  ▼
Authentication & Authorization (cryptographic signature verification, claims, scopes)
  │
  ▼
Schema validation & sanitization (payload shape, type coercion, field constraints)
  │
  ▼
Application / Use-case service (orchestration, idempotency store check)
  │
  ▼
Domain business invariants (catalog stock check, customer credit limits)
  │
  ▼
Database transaction boundary (ACID isolation, row-level locks, rollback guarantees)
  │
  ▼
Transactional Outbox record (atomic event staging to prevent dual-write bugs)
  │
  ▼
Cache invalidation / asynchronous background job dispatch
  │
  ▼
Response serialization (DTO formatting, HTTP status 201 Created)
  │
  ▼
Socket transmit (sendall, TCP FIN/keep-alive)
```

And critically, explain:
- **What each layer does** and why it exists.
- **What can fail** (socket timeout, lock contention, downstream partition, poison pill).
- **What should be retried** (transient 503s with exponential backoff and jitter).
- **What must never be retried** without an idempotency key (non-idempotent `POST /orders`).
- **What must be transactional** (inventory deduction + order insertion + outbox event).
- **What must be asynchronous** (dispatching third-party confirmation emails/webhooks).
- **What should be cached** (catalog product metadata, user permissions) and how cache consistency is maintained.
- **What metrics and logs are required** (RED metrics: Rate, Errors, Duration; structured JSON logs with correlation IDs).
- **What races under concurrency** (inventory overselling, double-booking, balance deductions).
- **How the system is operated, containerized, and deployed** with health probes (`/healthz`, `/readyz`).

---

## The Core Learning Loop

Every phase follows a disciplined, empirical engineering workflow:

```text
MOTTO
  ↓
PROBLEM           (Concrete challenge or production limitation)
  ↓
PREDICT           (Formulate explicit hypothesis before coding)
  ↓
FIRST PRINCIPLES  (OS sockets, TCP byte streams, ACID guarantees)
  ↓
MENTAL MODEL      (Diagrammatic request flow and boundaries)
  ↓
BUILD SIMPLE      (Custom implementation without external libraries)
  ↓
USE REAL TOOL     (Adopt industry tools: FastAPI, PostgreSQL, Redis)
  ↓
TEST              (Pytest assertions verifying invariants and edge cases)
  ↓
INSPECT           (Inspect raw bytes, SQL logs, network states)
  ↓
MEASURE           (Benchmark throughput, latency percentiles p50/p95/p99)
  ↓
BREAK             (Inject faults: packet drops, connection loss, timeouts)
  ↓
DEBUG             (Diagnose root cause using logs and stack traces)
  ↓
IMPROVE           (Apply resilience patterns: retries, breakers, outbox)
  ↓
EVIDENCE          (Record empirical observations in evidence log)
```

---

## Repository Map

```text
backend-engineering-from-scratch/
├── phases/                  # 190 complete phases (Phase 00 through Phase 189)
│   ├── 00-backend-engineering-lab/
│   ├── 02-build-a-tcp-server/
│   ├── 03-build-a-minimal-http-server/
│   ├── 09-routing-from-scratch/
│   ├── 14-middleware-from-first-principles/
│   ├── 20-connection-pooling/
│   ├── 35-password-storage/
│   ├── 37-token-based-authentication/
│   └── ... [190 phases across 19 parts]
│
├── projects/                # 13 Substantial Standalone Projects
│   ├── 01-url-shortener/               # Base62 encoding, caching, click telemetry
│   ├── 02-todo-api/                    # Clean Architecture with ownership checks
│   ├── 03-blog-platform/               # Relational data model, eager query loading
│   ├── 04-ecommerce-backend/           # Atomic order placement, inventory reservation
│   ├── 05-booking-backend/             # High-concurrency slot holds, double-booking defense
│   ├── 06-notification-service/        # Multi-provider failover, templating
│   ├── 07-file-processing-service/     # Storage tracking, async worker pipeline
│   ├── 08-analytics-event-api/         # High-throughput batch buffering, backpressure
│   ├── 09-webhook-delivery-platform/   # HMAC-SHA256 signatures, retry policies
│   ├── 10-multi-tenant-saas-backend/   # Row-level tenant isolation, audit trails
│   ├── 11-real-time-chat-backend/      # WebSocket rooms, broadcasting
│   ├── 12-rate-limiting-service/       # Token Bucket, Sliding Window algorithms
│   └── 13-authentication-service/      # Bcrypt hashing, JWTs, refresh token rotation
│
├── broken-systems/          # 32 Broken-Backend Debugging Labs
│   ├── lab-01-connection-leak-pool-exhaustion/
│   ├── lab-02-unindexed-query-lock-escalation/
│   ├── lab-03-blocking-dns-resolution/
│   ├── lab-08-database-deadlock-concurrent-updates/
│   ├── lab-12-n-plus-one-query-explosion/
│   ├── lab-16-jwt-alg-none-signature-bypass/
│   ├── lab-20-retry-storm-thundering-herd/
│   ├── lab-23-dual-write-inconsistency/
│   └── ... [32 hands-on defect reproduction & fix labs]
│
├── apps/                    # 4 Production Capstones
│   ├── 01_modular_monolith/             # Users, Catalog, Orders, Transactional Outbox
│   ├── 02_failure_driven_backend/       # Chaos injection, Circuit Breakers, Fallbacks
│   ├── 03_extracted_notification_service/# Independent worker, Deduplication, DLQ
│   └── 04_production_readiness_review/  # Health probes, Security audit, PRR report
│
├── benchmarks/              # Performance Benchmark Harness
│   ├── benchmark_sync_vs_async.py
│   ├── benchmark_connection_pooling.py
│   ├── benchmark_cache_aside.py
│   ├── benchmark_json_serialization.py
│   ├── benchmark_cursor_vs_offset.py
│   └── run_all_benchmarks.py
│
├── load-tests/              # Async High-Concurrency Load Generator
│   ├── load_test_runner.py              # RPS, p50, p90, p95, p99 calculator
│   └── scenarios/
│       ├── orders_spike.py              # Flash-sale inventory contention
│       └── read_heavy_traffic.py        # 90% read / 10% write traffic distribution
│
├── docs/                    # Deep Engineering Guides & Mental Models
│   ├── mental-models.md                 # 10 Core mental models of backend engineering
│   ├── request-lifecycle.md             # The 12-hop lifecycle of POST /orders
│   ├── api-design.md                    # REST, RPC, GraphQL, idempotency, versioning
│   ├── debugging.md                     # Systematic debugging playbook & triage
│   ├── production-checklist.md          # 50-point production deployment checklist
│   └── glossary.md                      # Backend engineering terminology
│
├── scripts/                 # Automation & Environment Checkers
│   ├── check-environment.sh             # Validates Python, tools, and system specs
│   ├── start-dev.sh                     # Starts local development servers
│   ├── reset-db.sh                      # Cleans and initializes persistence stores
│   └── run-tests.sh                     # Executes repository test suites
│
├── ROADMAP.md               # Complete syllabus: 19 parts, 190 phases
├── LEARNING.md              # Empirical learning methodology & completion standards
├── LESSON_TEMPLATE.md       # Structural blueprint for every lesson
├── VERSIONS.md              # Verified dependency versions & runtime baselines
├── SECURITY.md              # Vulnerability reporting & security practices
├── CONTRIBUTING.md          # Contribution guidelines & coding conventions
└── Makefile                 # Command center for setup, test, and benchmarks
```

---

## Curriculum Overview (19 Parts, 190 Phases)

The curriculum is structured into 19 progressive parts covering every dimension of backend engineering:

| Part | Title | Phases | Core Concepts |
| :--- | :--- | :--- | :--- |
| **01** | Foundations of Networked Systems | 00–09 | BSD Sockets, TCP 3-way handshakes, HTTP/1.1 wire protocol, Request lifecycle, Dynamic routing |
| **02** | APIs, Contracts, and Validation | 10–19 | Framework introduction, Schema validation, OpenAPI, Onion middleware pipeline, Dependency injection |
| **03** | Persistence, Transactions, & ORMs | 20–29 | Connection pooling, SQL schema design, ACID isolation levels, Deadlocks, Query optimization, Migrations |
| **04** | Authentication, Sessions, & Access | 30–39 | Password hashing (Bcrypt/Argon2), Cookie sessions, JWT RFC 7519, RBAC, OAuth2/OIDC, Multi-factor auth |
| **05** | Caching & Performance Optimization | 40–49 | Cache-Aside, Write-Through, Cache stampedes, Thundering herds, Redis data structures, Cache invalidation |
| **06** | Asynchronous Work & Queues | 50–59 | Worker loops, Message brokers, At-least-once delivery, Idempotent consumers, Dead Letter Queues (DLQ) |
| **07** | Concurrency & Race Conditions | 60–69 | Thread safety, Asyncio event loop blocking, Optimistic vs Pessimistic locking, Distributed locks |
| **08** | Reliability & Fault Tolerance | 70–79 | Timeouts, Retries with exponential backoff & jitter, Circuit Breakers, Bulkheading, Rate limiting |
| **09** | Observability, Metrics, & Logs | 80–89 | Structured JSON logging, RED metrics, Distributed tracing (W3C TraceContext), Alert thresholds |
| **10** | Backend Security & Hardening | 90–99 | OWASP Top 10, SQLi, SSRF, IDOR, CORS, CSRF, Constant-time secrets, Cryptographic key rotation |
| **11** | Testing & Verification Strategies | 100–109 | Unit tests, Integration tests, Test containers, Mocking boundaries, Contract tests, Mutation testing |
| **12** | Scalability & Load Management | 110–119 | Horizontal scaling, Stateless backends, Load balancing algorithms, Connection draining, Sharding |
| **13** | Event-Driven Architectures | 120–129 | Pub/Sub, Transactional Outbox pattern, Event sourcing, CQRS, Change Data Capture (CDC), Kafka/Pulsar |
| **14** | API Protocols & Real-Time | 130–139 | WebSockets, Server-Sent Events (SSE), HTTP/2 multiplexing, gRPC/Protobuf, GraphQL, Webhooks |
| **15** | Data Consistency & Distributed State | 140–149 | CAP theorem, PACELC, 2-Phase Commit, Saga pattern (Orchestration vs Choreography), Vector clocks |
| **16** | Containerization & Cloud Native | 150–159 | Docker multi-stage builds, Distroless images, Signal handling (SIGTERM), 12-Factor app config, K8s probes |
| **17** | CI/CD & Safe Deployments | 160–169 | Automated test gates, Blue/Green deployments, Canary releases, Feature flags, Zero-downtime migrations |
| **18** | Production Operations & SRE | 170–179 | SLOs/SLAs/SLIs, Error budgets, Incident management, Runbooks, Disaster recovery, Capacity planning |
| **19** | System Design Synthesis | 180–189 | High-concurrency booking engines, Payment gateways, Multi-tenant SaaS, Rate limiting clusters |

*See [ROADMAP.md](ROADMAP.md) for the detailed phase-by-phase breakdown.*

---

## 32 Broken-Backend Debugging Labs

Real learning happens when production breaks at 3 AM. The `broken-systems/` directory contains 32 dedicated debugging laboratories. Each lab includes a reproducible defect, a failing test reproducing the symptom, a diagnosed root cause, and a verified architectural fix:

| Lab | Defect Category | Root Cause & Mechanism | Fix Applied |
| :--- | :--- | :--- | :--- |
| **lab-01** | Resources | Unclosed database connections under exceptions | RAII context manager / pool return guarantee |
| **lab-02** | Database | Full table scan triggering shared row lock escalation | B-Tree index creation on lookup columns |
| **lab-03** | Networking | Synchronous DNS resolution blocking worker loop | Async DNS resolver with local TTL cache |
| **lab-04** | Concurrency | Thread-unsafe shared mutable global dictionary | Mutual exclusion locks / process isolation |
| **lab-05** | Queues | Ingestion rate > processing rate without backpressure | Bounded queue with HTTP 429 rejection |
| **lab-06** | Queues | Worker retry processing non-idempotent duplicate job | Atomic idempotency key deduplication check |
| **lab-07** | Caching | Write to DB without invalidating Redis cache | Transactional write-through cache eviction |
| **lab-08** | Database | Two transactions acquiring row locks in reverse order | Canonical lock ordering enforcement |
| **lab-11** | Async/IO | Calling synchronous `time.sleep` in async route | `asyncio.sleep` / thread-pool offloading |
| **lab-12** | Database | Fetching parent rows, then issuing N child queries | Eager SQL JOIN / aggregated batch loading |
| **lab-13** | Security | String concatenation in SQL statements | Parameterized queries with prepared statements |
| **lab-16** | Security | Unverified JWT accepting `{"alg": "none"}` | Explicit cryptographic algorithm enforcement |
| **lab-17** | Concurrency | Concurrent read-modify-write losing financial balance | Atomic `UPDATE balance = balance - ?` |
| **lab-20** | Networking | 1,000 clients retrying simultaneously on outage | Truncated exponential backoff with full jitter |
| **lab-21** | Resilience | Circuit breaker remaining OPEN forever after failure | Half-open probe transition after cooldown |
| **lab-23** | Consistency | Writing to database succeeds, Kafka publish fails | Transactional Outbox pattern |
| **lab-25** | Load | Sudden traffic surge exhausting process memory | Leaky bucket rate limiter at gateway |
| **lab-28** | Multi-Tenancy | Query omitting `tenant_id` filter across accounts | Mandatory tenant scoping in repository layer |
| **lab-31** | Database | `OFFSET 50000` scanning and discarding 50,000 rows | Keyset / Cursor pagination (`WHERE id > cursor`) |

*Execute all broken-system reproduction and verification tests with `make test-broken`.*

---

## 4 Production Capstones

The `apps/` directory contains four capstone implementations:

1. **`01_modular_monolith`**:
   - Clean domain separation between `users`, `catalog`, `orders`, and `notifications`.
   - Shared SQLite/PostgreSQL persistence with atomic multi-table transactions.
   - **Transactional Outbox Pattern**: Order creation and outbox staging occur within a single database transaction, completely eliminating dual-write inconsistencies.
   - Built-in RED metrics engine and structured JSON logging with correlation IDs.

2. **`02_failure_driven_backend`**:
   - Integrated chaos injection suite simulating sudden database drops, query timeouts, and cache network partitions.
   - Self-healing resilience: **Circuit Breaker** state machine (`CLOSED` -> `OPEN` -> `HALF_OPEN`) fast-failing downstream calls, and **Cache-Aside Degradation** that automatically serves from DB when Redis crashes.

3. **`03_extracted_notification_service`**:
   - Demonstrates extracting notification functionality out of the monolith into an independent asynchronous service.
   - Idempotent consumer engine with deduplication storage, multi-provider delivery adapters, and **Dead Letter Queue (DLQ)** isolation for poison messages.

4. **`04_production_readiness_review`**:
   - An automated audit engine that validates services against 5 production pillars: secret entropy, health/readiness probes (`/healthz`, `/readyz`), CORS restrictions, observability pipelines, and timeout boundaries. Generates an executive PRR scorecard.

---

## Quickstart & First Commands

### Prerequisites
- Python 3.12+ (verified LTS baseline)
- `curl`, `git`, `make`
- Docker (optional, for external service testing)

### Setup & Verification

```bash
# 1. Clone repository
git clone https://github.com/rohitg00/backend-engineering-from-scratch.git
cd backend-engineering-from-scratch

# 2. Set up virtual environment and install dependencies
make setup

# 3. Verify your environment passes all prerequisites
make env-check
```

### Running Test Suites

```bash
# Run all 841 tests across phases, projects, broken systems, and capstone apps
make test

# Run tests by category
make test-phases     # Tests core phases from socket to auth
make test-projects   # Tests all 13 standalone projects
make test-broken     # Tests all 32 broken system reproduction & fixes
make test-apps       # Tests all 4 production capstone applications
```

### Running Performance Benchmarks

Execute the automated benchmark harness to measure concurrency, pooling, and latency:

```bash
make benchmarks
```

Sample Benchmark Output:
```text
▶ Benchmark: Sync vs Async Concurrency (I/O Bound)
    • tasks: 25 | sync: 0.154s | async: 0.005s | speedup: 26.54x
▶ Benchmark: Connection Overhead vs Connection Reuse
    • queries: 250 | without pool: 0.016s | with pool: 0.0001s | speedup: 111.46x
▶ Benchmark: Cache Hit vs Database Latency
    • iterations: 500 | db: 0.133s | cache: 0.00001s | speedup: 12,271x
▶ Benchmark: JSON Serialization / Deserialization Throughput
    • throughput: 174,255 ops/sec | payload: 1,054 bytes
▶ Benchmark: Cursor/Keyset vs Deep OFFSET Pagination
    • offset 20000: 0.0034s | cursor seek: 0.0002s | speedup: 16.76x
```

### Running Asynchronous Load Tests

Simulate realistic high-concurrency production load:

```bash
make load-test
```

Simulates flash-sale inventory contention (200 concurrent requests competing for 20 units) and read-heavy traffic (90% reads, 10% writes), asserting exact transactional consistency and reporting throughput (RPS) alongside p50, p90, p95, and p99 latency percentiles.

---

## The 10 Mental Models of Backend Engineering

1. **The Request is a State Transition**: An HTTP request is not a function call; it is a networked command or query attempting to transition system state.
2. **Network Calls Always Fail Eventually**: If code touches a socket, assume it will timeout, drop packets, or reset.
3. **The Database is the Source of Truth, Caches are Ephemeral**: Never write to cache first without a plan for consistency and invalidation.
4. **Transactions are Consistency Boundaries**: Group state changes that must succeed or fail together into atomic ACID transactions.
5. **Never Use Two-Phase Commit When An Outbox Will Do**: The Transactional Outbox pattern guarantees eventual consistency without distributed coordinator locks.
6. **Averages Lie; Only Percentiles Matter**: High-volume backends with multi-dependency fan-outs are governed by p95 and p99 latency.
7. **Idempotency is the Bedrock of Distributed Systems**: If a client can retry, the server must ensure duplicate executions cause zero duplicate side-effects.
8. **Asynchronous Decoupling Protects the Critical Path**: Do only what is strictly necessary before returning the HTTP response; delegate the rest to background queues.
9. **Defense in Depth**: Authenticate at the boundary, authorize at the use case, validate at the schema, and constrain at the database column.
10. **Operability Over Cleverness**: Code is read and operated far more often than it is written. Structured logs, metrics, and simple architectures beat clever tricks.

---

## Contributing & Community

Contributions that enhance explanations, add empirical failure injection scenarios, or sharpen first-principles demonstrations are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and our [SECURITY.md](SECURITY.md) guidelines.

---

## License

This educational repository is distributed under the MIT License. See [LICENSE](LICENSE) for details.
