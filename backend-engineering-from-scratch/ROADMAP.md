# Backend Engineering Roadmap (Phases 00 – 189)

> **Understand it. Build it. Serve it. Persist it. Break it. Debug it. Secure it. Scale it. Operate it.**

A structured 190-phase curriculum taking a developer from raw network sockets to distributed, production-grade, observable backend services.

---

## Curriculum Structure Overview

```text
Sockets & HTTP Fundamentals (Phases 00-15)
           │
           ▼
Application Architecture & Domain Rules (Phases 16-17)
           │
           ▼
Databases, Persistence & Transactions (Phases 18-33)
           │
           ▼
Authentication, Authorization & Security (Phases 34-46)
           │
           ▼
Caching & Data Consistency (Phases 47-50)
           │
           ▼
Background Work, Queues & Events (Phases 51-63)
           │
           ▼
Reliability, Resilience & Fault Tolerance (Phases 64-69)
           │
           ▼
Concurrency Models & I/O Performance (Phases 70-80)
           │
           ▼
API Evolution, Protocols & Real-Time (Phases 81-88)
           │
           ▼
Observability, Telemetry & Operations (Phases 89-96)
           │
           ▼
Testing Strategy & Verification (Phases 97-102)
           │
           ▼
Performance, Bottlenecks & Diagnostics (Phases 103-110)
           │
           ▼
Configuration, Deployment & Containers (Phases 111-126)
           │
           ▼
Advanced Security, Tenancy & Resilience (Phases 127-144)
           │
           ▼
Monolith to Distributed Systems (Phases 145-155)
           │
           ▼
Capacity, Estimation & Anti-Patterns (Phases 156-159)
           │
           ▼
Production Debugging Labs (Phases 160-170)
           │
           ▼
Substantial Backend Projects (Phases 171-183)
           │
           ▼
Capstones, System Design & Final Synthesis (Phases 184-189)
```

---

## Part 1: Sockets, HTTP & Protocol Fundamentals (Phases 00 – 15)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **00** | `00-backend-engineering-lab` | Backend Engineering Lab | Inspecting Python runtime, process descriptors, loopback sockets, and persistence. |
| **01** | `01-what-is-a-backend` | What Is a Backend? | State machine, business invariants, untrusted client boundaries, and persistence. |
| **02** | `02-build-a-tcp-server` | Build a TCP Server | BSD socket API (`bind`, `listen`, `accept`, `recv`, `sendall`) over raw TCP streams. |
| **03** | `03-build-a-minimal-http-server` | Build a Minimal HTTP Server | RFC 9112 textual framing, CRLF splitting, request-line, headers, and body. |
| **04** | `04-http-request-lifecycle` | HTTP Request Lifecycle | Tracing bytes from socket to parser, DTO, router, handler, response, and wire. |
| **05** | `05-http-methods` | HTTP Methods | RFC 9110 method semantics: Safe (GET/HEAD), Idempotent (PUT/DELETE), Unsafe (POST). |
| **06** | `06-status-codes` | Status Codes | 2xx success, 4xx client errors, 5xx server outages; why returning 200 for errors is fatal. |
| **07** | `07-headers` | Headers | Metadata negotiation (`Content-Type`, `Accept`, `Authorization`, `Idempotency-Key`). |
| **08** | `08-json-apis` | JSON APIs | Wire representation vs typed domain entities; handling malformed JSON safely. |
| **09** | `09-routing-from-scratch` | Routing From Scratch | Building method/path dispatch structures (Trie/Regex) before framework routing. |
| **10** | `10-introduce-web-framework` | Introduce Web Framework | Mapping ASGI scope/receive/send and FastAPI decorators to first principles. |
| **11** | `11-request-validation` | Request Validation | Boundary validation vs domain validation; schema types, lengths, and constraints. |
| **12** | `12-api-contracts` | API Contracts | Why public API schemas must remain strictly independent of database column models. |
| **13** | `13-error-responses` | Error Responses | Standardizing machine-readable problem details (RFC 9457) and redacting stack traces. |
| **14** | `14-middleware-from-first-principles` | Middleware From First Principles | Onion-style request pipeline execution for correlation IDs, access logs, and CORS. |
| **15** | `15-dependency-injection` | Dependency Injection | Inversion of Control; passing repositories and sessions explicitly for testability. |

---

## Part 2: Application Architecture & Domain Design (Phases 16 – 17)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **16** | `16-application-architecture` | Application Architecture | Layered architecture: HTTP transport -> Use-Case service -> Domain model -> Repository. |
| **17** | `17-business-logic-vs-http-logic` | Business Logic vs HTTP Logic | Decoupling business rules from HTTP request objects for sub-millisecond unit testing. |

---

## Part 3: Databases, Persistence & Transactions (Phases 18 – 33)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **18** | `18-postgresql-integration` | PostgreSQL Integration | Connecting application to relational database via socket protocol and raw SQL. |
| **19** | `19-database-connections` | Database Connections | Connection lifecycle; measuring 3-way handshake and SSL setup costs per query. |
| **20** | `20-connection-pooling` | Connection Pooling | Managing bounded pools; handling pool starvation, queueing, and timeouts. |
| **21** | `21-repository-boundary` | Repository Boundary | Encapsulating SQL queries behind domain repository interfaces. |
| **22** | `22-crud-correctly` | CRUD Correctly | Handling missing rows, conflicts, partial updates, and database constraints cleanly. |
| **23** | `23-transactions` | Transactions | Multi-row consistency; simulating power loss/crash between steps to derive ACID. |
| **24** | `24-transaction-boundaries` | Transaction Boundaries | Scoping transactions tightly to business consistency boundaries; avoiding mega-transactions. |
| **25** | `25-isolation-and-concurrent-requests` | Isolation and Concurrent Requests | Dirty reads, non-repeatable reads, phantom reads; database isolation levels. |
| **26** | `26-optimistic-concurrency` | Optimistic Concurrency | Version numbers and conditional updates (`WHERE version = :expected`) to stop lost updates. |
| **27** | `27-database-constraints-as-defense` | Database Constraints as Defense | UNIQUE, FOREIGN KEY, and CHECK constraints preventing application race conditions. |
| **28** | `28-orm-introduction` | ORM Introduction | Introducing SQLAlchemy after raw SQL; inspecting generated SQL queries. |
| **29** | `29-n-plus-one-problem` | N+1 Problem | Detecting query explosions with 1 parent query + N child queries; fixing with JOINs. |
| **30** | `30-database-migrations` | Database Migrations | Version-controlled schema evolutions; tracking migration history tables. |
| **31** | `31-pagination` | Pagination | Offset pagination latency decay at deep scans vs constant-time Keyset/Cursor pagination. |
| **32** | `32-filtering-and-sorting-apis` | Filtering and Sorting APIs | Whitelisting query parameters; preventing dynamic SQL injection in ORDER BY clauses. |
| **33** | `33-search-basics` | Search Basics | Full-text search with SQL LIKE, GIN indexes, and tsvector before introducing search clusters. |

---

## Part 4: Authentication, Authorization & Security (Phases 34 – 46)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **34** | `34-authentication-problem` | Authentication Problem | Proving caller identity; separating AuthN (who are you?) from AuthZ (what can you do?). |
| **35** | `35-password-storage` | Password Storage | Salted adaptive work-factor hashing with bcrypt/Argon2; why MD5/SHA256 fail. |
| **36** | `36-session-based-authentication` | Session-Based Authentication | Server-side session stores, session IDs, and secure cookie attributes (HttpOnly, SameSite). |
| **37** | `37-token-based-authentication` | Token-Based Authentication | Signed bearer tokens (JWT RFC 7519); verifying HMAC/RSA signatures; expiration. |
| **38** | `38-authorization` | Authorization | Permission models: User -> Role -> Permission -> Resource evaluation. |
| **39** | `39-rbac` | RBAC | Role-Based Access Control; role hierarchies and their architectural limitations. |
| **40** | `40-resource-based-authorization` | Resource-Based Authorization | Object-level access control: verifying that caller owns or collaborates on the resource. |
| **41** | `41-api-security-basics` | API Security Basics | Defense-in-depth: validation, auth, rate limiting, least privilege, and security headers. |
| **42** | `42-sql-injection` | SQL Injection | Exploiting raw SQL string concatenation locally and fixing via parameterized queries. |
| **43** | `43-cors` | CORS | Cross-Origin Resource Sharing; preflight OPTIONS; why CORS is a browser boundary. |
| **44** | `44-csrf` | CSRF | Cross-Site Request Forgery in cookie-based apps; Double-Submit Cookie defense. |
| **45** | `45-rate-limiting-from-scratch` | Rate Limiting From Scratch | In-memory token bucket and fixed window algorithms to prevent brute-force abuse. |
| **46** | `46-distributed-rate-limiting` | Distributed Rate Limiting | Shared rate limiting across multiple backend nodes using Redis atomic operations. |

---

## Part 5: Caching & Data Consistency (Phases 47 – 50)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **47** | `47-why-caching-exists` | Why Caching Exists | Tradeoff: Trading memory and data freshness for latency and database load reduction. |
| **48** | `48-cache-aside` | Cache-Aside | Read path: Cache Hit -> return; Cache Miss -> query DB -> write to cache with TTL. |
| **49** | `49-cache-invalidation` | Cache Invalidation | The stale data problem; write-through, explicit invalidation, and TTL expiration. |
| **50** | `50-cache-stampede` | Cache Stampede | Thundering herd on expired hot keys; single-flight locking and TTL jitter mitigations. |

---

## Part 6: Background Work, Queues & Events (Phases 51 – 63)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **51** | `51-background-work-problem` | Background Work Problem | Synchronous slow work (emails, PDF generation) stalling HTTP requests and exhausting workers. |
| **52** | `52-in-process-background-work` | In-Process Background Work | Python `asyncio.create_task` and FastAPI `BackgroundTasks`; process crash vulnerability. |
| **53** | `53-durable-queue` | Durable Queue | Persistent task queues that survive application process restarts. |
| **54** | `54-worker-architecture` | Worker Architecture | Producer-Consumer pattern: API enqueues job payloads; dedicated workers consume. |
| **55** | `55-retry` | Retry | Handling transient worker failures; retry limits and backoff schedules. |
| **56** | `56-idempotent-jobs` | Idempotent Jobs | Guaranteeing that executing a job twice produces exactly one side effect. |
| **57** | `57-dead-letter-queue` | Dead-Letter Queue | Isolating unprocessable "poison pill" tasks without crashing worker loops. |
| **58** | `58-scheduling-work` | Scheduling Work | Recurring jobs: cron vs application schedulers vs queue delay timers. |
| **59** | `59-events-vs-commands` | Events vs Commands | Intent to mutate (`SendEmailCommand`) vs notification of state change (`OrderPlaced`). |
| **60** | `60-domain-application-events` | Domain/Application Events | Decoupling in-process side effects via publisher-subscriber event buses. |
| **61** | `61-external-event-broker` | External Event Broker | Bridging event communication across microservice boundaries. |
| **62** | `62-transactional-outbox` | Transactional Outbox | Eliminating the dual-write problem by saving outbox events in the same SQL transaction. |
| **63** | `63-idempotency-keys` | Idempotency Keys | Safely handling client retries on `POST /payments` using deduplication tokens. |

---

## Part 7: Reliability, Resilience & Fault Tolerance (Phases 64 – 69)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **64** | `64-timeouts` | Timeouts | Connect timeouts, read timeouts, and request deadlines on every outbound call. |
| **65** | `65-retries` | Retries | When retrying is safe (idempotent + transient failure) and when it is destructive. |
| **66** | `66-exponential-backoff-and-jitter` | Exponential Backoff and Jitter | Preventing retry storms by adding randomized delays to backoff curves. |
| **67** | `67-circuit-breaker` | Circuit Breaker | Closed, Open, Half-Open state machine tripping fast failures on degraded services. |
| **68** | `68-bulkheads` | Bulkheads | Partitioning thread and connection pools so one failing service cannot sink the whole app. |
| **69** | `69-graceful-degradation` | Graceful Degradation | Returning cached or degraded fallbacks when non-critical dependencies fail. |

---

## Part 8: Concurrency Models & I/O Performance (Phases 70 – 80)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **70** | `70-concurrency-model` | Concurrency Model | Processes vs OS Threads vs Event Loop Asyncio; the Python GIL. |
| **71** | `71-sync-server` | Sync Server | Blocking single-threaded request processing; observing concurrency bottlenecks. |
| **72** | `72-threaded-server` | Threaded Server | Multi-threaded concurrency; thread memory overhead and context switching costs. |
| **73** | `73-async-server` | Async Server | Cooperative non-blocking I/O multiplexing via epoll/kqueue event loops. |
| **74** | `74-blocking-inside-async` | Blocking Inside Async | Invoking `time.sleep()` in an async handler; event loop starvation and latency explosion. |
| **75** | `75-cpu-bound-work` | CPU-Bound Work | Handling heavy computation without stalling the web server via ProcessPoolExecutor. |
| **76** | `76-backpressure` | Backpressure | Signaling upstream producers when downstream processing buffers reach capacity. |
| **77** | `77-bounded-queues` | Bounded Queues | Unbounded queues cause OOM crashes; bounded queues enforce explicit load rejection. |
| **78** | `78-uploads` | Uploads | Streaming multipart/form-data uploads to disk without buffering gigabytes into RAM. |
| **79** | `79-object-storage` | Object Storage | Storing file metadata in relational SQL and raw binary blobs in S3-compatible stores. |
| **80** | `80-download-streaming` | Download Streaming | Streaming large files in chunked responses to maintain low memory footprints. |

---

## Part 9: API Evolution, Protocols & Real-Time (Phases 81 – 88)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **81** | `81-api-versioning` | API Versioning | URI versioning (`/v1`) vs Header versioning; deprecation lifecycles. |
| **82** | `82-backward-compatibility` | Backward Compatibility | Additive schema evolutions; preventing breaking changes for mobile/third-party clients. |
| **83** | `83-openapi` | OpenAPI | Generating and validating machine-readable contract specifications (OpenAPI 3.1). |
| **84** | `84-rest-design` | REST Design | Pragmatic resource modeling, uniform interfaces, and RFC-compliant status codes. |
| **85** | `85-rpc-grpc-concepts` | RPC / gRPC Concepts | Strongly typed binary RPC protocols vs textual HTTP/JSON for internal microservices. |
| **86** | `86-websockets` | WebSockets | RFC 6455 HTTP upgrade handshake, persistent full-duplex TCP framing, and heartbeats. |
| **87** | `87-server-sent-events` | Server-Sent Events | Unidirectional server streaming via `text/event-stream` for live updates. |
| **88** | `88-long-polling` | Long Polling | Simulating push updates over standard HTTP connections; tradeoffs and connection costs. |

---

## Part 10: Observability, Telemetry & Operations (Phases 89 – 96)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **89** | `89-logging` | Logging | Structured JSON logging with timestamp, level, context, and automatic secret redaction. |
| **90** | `90-correlation-request-ids` | Correlation / Request IDs | Generating and propagating `X-Request-ID` across distributed services and logs. |
| **91** | `91-metrics` | Metrics | Counters, Gauges, and Histograms; instrumenting application health signals. |
| **92** | `92-latency-percentiles` | Latency Percentiles | Why arithmetic means deceive; calculating p50, p95, and p99 latency distributions. |
| **93** | `93-tracing` | Tracing | Distributed tracing: Spans, Traces, parent-child spans across network boundaries. |
| **94** | `94-red-method` | RED Method | Operational monitoring lens: Rate (RPS), Errors (failed count), Duration (latency). |
| **95** | `95-health-endpoints` | Health Endpoints | Distinguishing `/health/live` (process alive) from `/health/ready` (dependencies connected). |
| **96** | `96-observability-debugging` | Observability Debugging | Triangulating root causes of latency spikes using correlated logs, metrics, and traces. |

---

## Part 11: Testing Strategy & Verification (Phases 97 – 102)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **97** | `97-testing-pyramid-strategy` | Testing Pyramid / Strategy | Balancing Unit, Integration, API, and End-to-End tests for fast, reliable verification. |
| **98** | `98-unit-testing-business-logic` | Unit Testing Business Logic | Testing pure domain models and rules in microseconds without database or network I/O. |
| **99** | `99-repository-integration-tests` | Repository Integration Tests | Testing SQL queries against real database engines to verify constraints and transactions. |
| **100** | `100-api-tests` | API Tests | End-to-end HTTP request testing using `httpx.AsyncClient` verifying full status/body contracts. |
| **101** | `101-test-containers-disposable-dependencies` | Test Containers / Disposable Dependencies | Spinning up disposable Docker containers for isolated, clean integration test runs. |
| **102** | `102-property-and-edge-case-testing` | Property and Edge-Case Testing | Generating boundary tests (empty strings, extreme integers, unicode) to find hidden bugs. |

---

## Part 12: Performance, Bottlenecks & Diagnostics (Phases 103 – 110)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **103** | `103-load-testing` | Load Testing | Benchmarking RPS, concurrency limits, and latency percentiles under sustained traffic. |
| **104** | `104-first-bottleneck` | First Bottleneck | Systematically isolating whether saturation is caused by CPU, DB, Locks, or Network. |
| **105** | `105-database-performance` | Database Performance | Analyzing execution plans with `EXPLAIN ANALYZE`; adding indexes to turn Seq Scans to Index Scans. |
| **106** | `106-application-profiling` | Application Profiling | Profiling Python execution time with cProfile to find CPU hotspots. |
| **107** | `107-memory-leaks` | Memory Leaks | Diagnosing memory growth caused by unbounded global caches or unclosed resources. |
| **108** | `108-connection-leaks` | Connection Leaks | Identifying database connections that fail to return to the pool on exceptions. |
| **109** | `109-timeout-cascades` | Timeout Cascades | Diagnosing how a slow downstream dependency backs up worker queues and crashes upstream nodes. |
| **110** | `110-failure-injection` | Failure Injection | Deliberately severing network links, filling disks, and killing processes to test recovery. |

---

## Part 13: Configuration, Deployment & Containers (Phases 111 – 126)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **111** | `111-configuration` | Configuration | 12-factor configuration; validating environment variables at process startup. |
| **112** | `112-secrets` | Secrets | Secret injection via environment variables or secret vaults; excluding credentials from Git. |
| **113** | `113-12-factor-concepts` | 12-Factor Concepts | Stateless processes, explicit dependencies, port binding, and disposable runtimes. |
| **114** | `114-graceful-shutdown` | Graceful Shutdown | Intercepting `SIGTERM`, stopping ingress, finishing in-flight requests, and closing pools. |
| **115** | `115-process-model` | Process Model | Multi-worker process architectures (Gunicorn/Uvicorn); memory isolation across workers. |
| **116** | `116-reverse-proxy` | Reverse Proxy | Nginx/Caddy fronting application servers: TLS termination, buffering, and security headers. |
| **117** | `117-load-balancing` | Load Balancing | Distributing requests across replicas; health checks and removing unhealthy nodes. |
| **118** | `118-stateless-backend` | Stateless Backend | Storing sessions in shared datastores (Redis) so any backend replica can serve any request. |
| **119** | `119-containerize-backend` | Containerize Backend | Writing production multi-stage Dockerfiles with non-root security privileges. |
| **120** | `120-docker-compose-application-stack` | Docker Compose Stack | Orchestrating API, PostgreSQL, Redis, and Background Worker with health dependencies. |
| **121** | `121-database-startup-dependency-failure` | Database Startup / Dependency Failure | Handling database unavailability at application boot via retry-with-backoff loops. |
| **122** | `122-migrations-during-deployment` | Migrations During Deployment | Safe sequencing: running schema migrations before or during rolling application releases. |
| **123** | `123-zero-downtime-migration-concepts` | Zero-Downtime Migration Concepts | Expand-Contract pattern: adding columns, backfilling data, deploying code, contracting old columns. |
| **124** | `124-ci-basics` | CI Basics | Continuous Integration pipelines: linting, type-checking, automated testing, and image builds. |
| **125** | `125-deployment-environments` | Deployment Environments | Managing Dev, Test, Staging, and Production environments without code branching. |
| **126** | `126-production-readiness` | Production Readiness | Evaluating applications against the comprehensive production readiness checklist. |

---

## Part 14: Advanced Security, Tenancy & Resilience (Phases 127 – 144)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **127** | `127-security-headers-https` | Security Headers / HTTPS | Enforcing HSTS, Content-Security-Policy, X-Frame-Options, and TLS encryption. |
| **128** | `128-dependency-security` | Dependency Security | Auditing Python packages for known CVE vulnerabilities and pinning dependencies. |
| **129** | `129-input-size-limits` | Input Size Limits | Rejecting oversized JSON bodies and large uploads before buffering to prevent DoS. |
| **130** | `130-abuse-and-resource-exhaustion` | Abuse and Resource Exhaustion | Throttling expensive endpoints, limiting page sizes, and preventing account enumeration. |
| **131** | `131-audit-logging` | Audit Logging | Immutable append-only audit logs recording who, what, when, and result for compliance. |
| **132** | `132-multi-tenancy` | Multi-Tenancy | Tenant isolation models: row-level `tenant_id` scoping vs schema isolation; preventing data leaks. |
| **133** | `133-soft-deletes` | Soft Deletes | Tradeoffs of `deleted_at` timestamps: query complexity, unique index collisions, and data retention. |
| **134** | `134-audit-history` | Audit History | Historical record versioning and change tracking patterns. |
| **135** | `135-webhooks` | Webhooks | Outbound webhook delivery engine: queuing, retries with exponential backoff, and DLQ. |
| **136** | `136-webhook-verification` | Webhook Verification | HMAC-SHA256 signature verification and replay prevention using timestamp windows. |
| **137** | `137-external-api-integration` | External API Integration | Defensive adapters around third-party APIs: timeouts, circuit breakers, and mock stubs. |
| **138** | `138-payment-like-workflow` | Payment-Like Workflow | State machine modeling: Pending -> Succeeded / Failed / Refunded with idempotency. |
| **139** | `139-file-processing-pipeline` | File Processing Pipeline | Uploading to storage, queuing processing task, background image/data transform, status update. |
| **140** | `140-notification-pipeline` | Notification Pipeline | Multi-channel notifications (Email, SMS, Push) with rate limiting and provider failover. |
| **141** | `141-search-integration` | Search Integration | Synchronizing relational database records with dedicated full-text search indexes. |
| **142** | `142-search-index-synchronization` | Search Index Synchronization | Asynchronous indexing via event streams; handling out-of-order index updates. |
| **143** | `143-cache-as-derived-data` | Cache as Derived Data | Treating caches as ephemeral, rebuildable projections of authoritative primary datastores. |
| **144** | `144-data-consistency-across-systems` | Data Consistency Across Systems | Establishing sources of truth across SQL, Redis, Search, and Event Brokers. |

---

## Part 15: Monolith to Distributed Systems (Phases 145 – 155)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **145** | `145-monolith-first` | Monolith First | The operational power of single deployables; avoiding premature distributed systems. |
| **146** | `146-modular-monolith` | Modular Monolith | Enforcing strict module boundaries and explicit internal interfaces within one deployable. |
| **147** | `147-when-to-split-a-service` | When to Split a Service | Justified service extraction: team autonomy, independent scaling, differing security domains. |
| **148** | `148-first-service-extraction` | First Service Extraction | Extracting a bounded subsystem; experiencing new costs (serialization, networks, deployments). |
| **149** | `149-remote-call-is-not-a-function-call` | Remote Call Is Not a Function Call | The Fallacies of Distributed Computing: network latency, partial failures, dropped packets. |
| **150** | `150-distributed-transaction-problem` | Distributed Transaction Problem | Why ACID transactions cannot cross network boundaries; Sagas and compensating actions. |
| **151** | `151-api-gateway-concept` | API Gateway Concept | Unified client entry point routing requests to internal microservices and handling auth. |
| **152** | `152-backend-for-frontend-concept` | Backend for Frontend (BFF) | Tailoring specialized backend aggregation layers for Mobile vs Web client requirements. |
| **153** | `153-feature-flags` | Feature Flags | Decoupling deployment from release; runtime toggles and cleaning up stale flags. |
| **154** | `154-canary-gradual-rollout-concepts` | Canary / Gradual Rollout Concepts | Routing 5% of traffic to a new version, monitoring error budgets, and automating rollback. |
| **155** | `155-error-budgets-reliability-thinking` | Error Budgets / Reliability | Service Level Objectives (SLOs) and Error Budgets as product requirements. |

---

## Part 16: Capacity, Estimation & Anti-Patterns (Phases 156 – 159)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **156** | `156-capacity-estimation` | Capacity Estimation | Calculating RPS, DB QPS, connection limits, network bandwidth, and storage from requirements. |
| **157** | `157-littles-law-intuition` | Little's Law Intuition | Concurrency = Arrival Rate x Latency ($L = \lambda \times W$); predicting server saturation. |
| **158** | `158-performance-budget` | Performance Budget | Decomposing request latency into network, app CPU, database, and cache allocations. |
| **159** | `159-backend-anti-patterns` | Backend Anti-Patterns | The comprehensive catalog of 25 fatal backend anti-patterns and their remedies. |

---

## Part 17: Production Debugging Labs (Phases 160 – 170)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **160** | `160-debugging-lab-slow-api` | Debugging Lab: Slow API | Diagnosing high p99 latency with low CPU caused by unindexed database table scans. |
| **161** | `161-debugging-lab-500-errors` | Debugging Lab: 500 Errors | Using structured log correlation IDs and tracebacks to isolate unhandled exceptions. |
| **162** | `162-debugging-lab-connection-pool-exhaustion` | Debugging Lab: Connection Pool Exhaustion | Identifying connection leaks in exception handlers and transactions held open during sleep. |
| **163** | `163-debugging-lab-redis-down` | Debugging Lab: Redis Down | Diagnosing application crashes when cache nodes fail; implementing fail-open degradation. |
| **164** | `164-debugging-lab-worker-lag` | Debugging Lab: Worker Lag | Diagnosing queue depth explosion when job processing time exceeds arrival rate. |
| **165** | `165-debugging-lab-duplicate-jobs` | Debugging Lab: Duplicate Jobs | Resolving duplicate billing charges caused by non-idempotent worker task retries. |
| **166** | `166-debugging-lab-stale-cache` | Debugging Lab: Stale Cache | Finding missing cache invalidation calls following database update mutations. |
| **167** | `167-debugging-lab-database-lock` | Debugging Lab: Database Lock | Inspecting active SQL transactions and deadlocks between concurrent row updates. |
| **168** | `168-debugging-lab-disk-full` | Debugging Lab: Disk Full | Diagnosing database write failures caused by unrotated application log file exhaustion. |
| **169** | `169-debugging-lab-dns-failure` | Debugging Lab: DNS Failure | Distinguishing external DNS resolution failure from network drops or application crashes. |
| **170** | `170-broken-backend-lab-set` | Broken Backend Lab Set | Overview and execution framework for the 32+ isolated failure scenarios in `broken-systems/`. |

---

## Part 18: End-to-End Backend Projects (Phases 171 – 183)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **171** | `171-project-url-shortener` | Project: URL Shortener | High-throughput redirect service: Base62 encoding, caching, collision handling, and metrics. |
| **172** | `172-project-todo-task-api` | Project: Todo / Task API | Clean architecture reference implementation: CRUD, ownership auth, pagination, and tests. |
| **173** | `173-project-blog-platform` | Project: Blog Platform | Relational modeling: Users, Posts, Comments, Likes; query optimization and N+1 prevention. |
| **174** | `174-project-ecommerce-backend` | Project: E-Commerce Backend | Multi-table ACID orders, inventory reservation, row-level locks, and outbox event publishing. |
| **175** | `175-project-booking-backend` | Project: Booking Backend | Concurrency crucible: Time slots, holds, expiration timers, and preventing double bookings. |
| **176** | `176-project-notification-service` | Project: Notification Service | Decoupled notification engine: templates, adapters (Email, SMS), retries, and rate limits. |
| **177** | `177-project-file-processing-service` | Project: File Processing Service | Async pipeline: multipart upload, metadata in SQL, blob in storage, worker thumbnailing. |
| **178** | `178-project-analytics-event-api` | Project: Analytics Event API | Ingestion engine: batch buffering, high-throughput writes, backpressure, and flush timers. |
| **179** | `179-project-webhook-delivery-platform` | Project: Webhook Delivery Platform | Outbound webhooks: subscriptions, event enqueueing, HMAC signing, retries, and DLQ. |
| **180** | `180-project-multi-tenant-saas-backend` | Project: Multi-Tenant SaaS Backend | Strict organizational tenant isolation, RBAC membership roles, and audit logging. |
| **181** | `181-project-real-time-chat-backend` | Project: Real-Time Chat Backend | WebSockets: connection registry, room broadcasting, message persistence, and presence. |
| **182** | `182-project-rate-limiting-service` | Project: Rate Limiting Service | Standalone rate limiter benchmarking Token Bucket, Sliding Window, and Leaky Bucket algorithms. |
| **183** | `183-project-authentication-service` | Project: Authentication Service | Security service: bcrypt registration, JWT issuance, refresh tokens, and password reset flows. |

---

## Part 19: Capstones, System Design & Final Synthesis (Phases 184 – 189)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **184** | `184-capstone-1-modular-monolith` | Capstone 1: Production Modular Monolith | Production-grade unified backend: Auth, Catalog, Orders, Notifications, Outbox, and Telemetry. |
| **185** | `185-capstone-2-failure-driven-backend` | Capstone 2: Failure-Driven Backend | Chaos engineering: injecting database drops, cache outages, and worker crashes on Capstone 1. |
| **186** | `186-capstone-3-extract-one-service` | Capstone 3: Extract One Service | Extracting the Notification Service from Capstone 1; implementing HTTP/event boundaries and retries. |
| **187** | `187-capstone-4-production-readiness-review` | Capstone 4: Production Readiness Review | Comprehensive architectural audit of Capstone 1 against the complete production checklist. |
| **188** | `188-backend-in-system-design` | Backend in System Design | The 18 fundamental architectural questions applied to any backend design problem. |
| **189** | `189-final-mental-model` | Final Mental Model | The ultimate synthesis: Tracing `POST /orders` from socket wire frames to database and workers. |

---

## Part 20: Advanced Distributed Protocols, Consensus, Storage & Security (Phases 190 – 205)

| Phase | Directory | Title | Core Concept / Question |
| :--- | :--- | :--- | :--- |
| **190** | `190-consensus-safety-and-quorum-math` | Consensus Safety and Quorum Math | In an asynchronous network, how does majority quorum overlap guarantee zero conflicting commits? |
| **191** | `191-raft-leader-election-and-heartbeats` | Raft Leader Election and Heartbeats | How do state transitions and randomized election timeouts prevent split-vote deadlocks? |
| **192** | `192-raft-log-replication-and-commit-index` | Raft Log Replication and Commit Index | How does the Log Matching Invariant safely repair divergent follower logs? |
| **193** | `193-two-phase-commit-and-saga-orchestrator` | Two-Phase Commit and Saga Orchestrator | When should you choose blocking 2PC locks vs asynchronous compensating Sagas? |
| **194** | `194-protobuf-wire-format-and-varints` | Protocol Buffers Wire Format and Varints | How does LEB128 varint and ZigZag bit-packing achieve high serialization density? |
| **195** | `195-http2-framing-and-stream-multiplexing` | HTTP/2 Framing and Stream Multiplexing | How do 9-byte binary frame headers eliminate Head-of-Line blocking across a single TCP socket? |
| **196** | `196-grpc-client-stub-and-deadlines` | gRPC Client Stub and Deadline Propagation | How does `grpc-timeout` header propagation prevent zombie compute in downstream dependencies? |
| **197** | `197-grpc-interceptors-and-load-balancing` | gRPC Interceptors and Load Balancing | How do onion-layer interceptors and client-side load balancing route multiplexed RPC streams? |
| **198** | `198-storage-engine-write-ahead-log` | Storage Engine Write-Ahead Log | How does binary WAL serialization with CRC32 checksums guarantee crash durability? |
| **199** | `199-lsm-memtable-and-sstable` | LSM-Tree MemTable and SSTable | How do sorted in-memory buffers and immutable SSTables convert random writes into sequential disk I/O? |
| **200** | `200-lsm-leveled-compaction` | LSM-Tree Leveled Compaction | How does multi-way merge sort bound read amplification and garbage-collect tombstones? |
| **201** | `201-btree-storage-engine-and-buffer-pool` | B+ Tree Storage Engine and Buffer Pool | How does a page-based B+ Tree and LRU Buffer Pool Manager minimize disk block fetches? |
| **202** | `202-cryptographic-hashing-and-hmac` | Cryptographic Hashing and HMAC | Why must webhook signatures and API MACs be verified using constant-time comparisons? |
| **203** | `203-symmetric-encryption-aes-gcm` | Symmetric Encryption and AEAD | How does AES-GCM provide authenticated encryption to prevent ciphertext tampering? |
| **204** | `204-tls-handshake-and-mtls-verification` | TLS Handshake and mTLS Verification | How does Mutual TLS turn network packets into verifiable cryptographic workload identities? |
| **205** | `205-zero-trust-paseto-and-service-identity` | Zero-Trust PASETO and Service Identity | How does PASETO eliminate JWT algorithm confusion attacks in zero-trust architectures? |
