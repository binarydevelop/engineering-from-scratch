# Backend Specifications, Protocol Standards & Runtime Baselines

> **Specification & Runtime Discipline**: In backend engineering, clarity on protocol RFCs, database consistency semantics, HTTP specifications, cryptographic primitives, and runtime toolchains is essential. We never treat framework convenience as a substitute for protocol comprehension.

---

## 1. Verified Environment & Tooling Baselines

The following versions have been empirically verified in this repository's development environment:

| Component | Target Baseline | Verified Local Version | Verification Command | Role in Curriculum |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | >= 3.12 LTS | **Python 3.12.14** (also 3.14.7) | `python3 --version` | Primary language for all from-scratch servers, concurrency, and apps |
| **FastAPI** | >= 0.115 | **0.141.1** | `python -c "import fastapi; print(fastapi.__version__)"` | Production framework introduced in Phase 10+ after from-scratch routing |
| **Starlette** | >= 0.40 | **1.7.0** | `python -c "import starlette; print(starlette.__version__)"` | Underlying ASGI toolkit powering request/response lifecycle |
| **Pydantic** | >= 2.9 | **2.13.5** | `python -c "import pydantic; print(pydantic.__version__)"` | Schema validation and serialization boundary |
| **Uvicorn** | >= 0.30 | **0.53.0** | `uvicorn --version` | Lightning-fast ASGI production web server |
| **HTTPX** | >= 0.27 | **0.28.1** | `python -c "import httpx; print(httpx.__version__)"` | Async and sync HTTP client for API testing and remote call experiments |
| **Pytest** | >= 8.3 | **9.1.1** | `pytest --version` | Test runner for all unit, integration, and failure injection tests |
| **Cryptography** | >= 43.0 | **50.0.1** | `python -c "import cryptography; print(cryptography.__version__)"` | Low-level cryptographic primitives and HMAC validation |
| **PyJWT** | >= 2.9 | **2.15.0** | `python -c "import jwt; print(jwt.__version__)"` | RFC 7519 JSON Web Token issuance and signature verification |
| **Bcrypt** | >= 4.2 | **5.0.0** | `python -c "import bcrypt; print(bcrypt.__version__)"` | Work-factor salted password hashing |
| **SQLite (Built-in)** | >= 3.40 | **3.53.1** | `python -c "import sqlite3; print(sqlite3.sqlite_version)"` | Zero-dependency transactional SQL engine for local persistence labs |
| **PostgreSQL (Target)**| >= 16.0 | **16.x / 17.x** | `docker run postgres:16-alpine` | Production ACID relational database with MVCC and transaction isolation |
| **Redis (Target)** | >= 7.2 | **7.2 / 7.4** | `docker run redis:7.2-alpine` | In-memory datastore for cache-aside, distributed rate-limiting, and streams |
| **Docker** | >= 24.0 | **29.7.2** | `docker --version` | Containerized runtime and local multi-service composition |
| **curl** | >= 8.0 | **8.7.1** | `curl --version` | CLI tool for raw HTTP inspection and request timing |

---

## 2. Protocol Standards & RFC Specifications

Every backend concept in this curriculum is mapped to its authoritative IETF RFC or formal specification:

| Domain | Protocol / Standard | Authoritative Specification | Key Directives & Mental Model |
| :--- | :--- | :--- | :--- |
| **Transport** | **TCP** | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) (supersedes RFC 793) | Three-way handshake (SYN, SYN-ACK, ACK), byte-stream abstraction, sliding window, flow control, TIME_WAIT state. |
| **Application** | **HTTP/1.1 Semantics** | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) | Resource semantics, HTTP methods (GET, POST, PUT, DELETE, PATCH), safe and idempotent operations. |
| **Application** | **HTTP/1.1 Framing** | [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112) | Request-line, CRLF formatting, header parsing, Content-Length vs Chunked Transfer-Encoding. |
| **Application** | **HTTP Caching** | [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) | Cache-Control directives (`no-cache`, `no-store`, `max-age`), conditional requests (`ETag`, `If-None-Match`). |
| **Security** | **HTTP Authentication** | [RFC 9110 Sec 11](https://www.rfc-editor.org/rfc/rfc9110#section-11) | Bearer token scheme, WWW-Authenticate challenge header, credential hygiene. |
| **Tokens** | **JSON Web Token (JWT)** | [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) | Compact, URL-safe means of representing claims; JWS signature verification; prevention of `none` algorithm vulnerability. |
| **Security** | **CORS** | [Fetch Living Standard (W3C/WHATWG)](https://fetch.spec.whatwg.org/#http-cors) | Cross-Origin Resource Sharing, Preflight `OPTIONS` requests, Origin header validation, credential handling. |
| **Security** | **Password Hashing** | [RFC 8018 (PBKDF2)](https://www.rfc-editor.org/rfc/rfc8018) / [RFC 9106 (Argon2)](https://www.rfc-editor.org/rfc/rfc9106) | Adaptive work-factor hashing algorithms, resistance to GPU brute-force attacks, unique cryptographic salt per user. |
| **WebSockets** | **WebSocket Protocol** | [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455) | HTTP Upgrade handshake (101 Switching Protocols), full-duplex persistent framing, ping/pong heartbeats. |
| **SSE** | **Server-Sent Events** | [HTML Living Standard 9.2](https://html.spec.whatwg.org/multipage/server-sent-events.html) | `text/event-stream` MIME type, unidirectional server streaming, automatic reconnection. |
| **Contracts** | **OpenAPI Specification** | [OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0) | Machine-readable API definition, JSON Schema integration, interactive documentation. |
| **Data Format** | **JSON** | [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) | Textual serialization standard, strict unicode handling, payload size limits. |

---

## 3. Specification vs. Implementation vs. Operational Reality

Throughout this curriculum, we maintain a strict tripartite distinction:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. PROTOCOL SPECIFICATION (IETF RFC)                                      │
│    What the standard formally demands (e.g., HTTP/1.1 message framing,    │
│    TCP FIN/ACK teardown, safe vs idempotent HTTP method definitions).     │
├───────────────────────────────────────────────────────────────────────────┤
│ 2. PYTHON RUNTIME & KERNEL IMPLEMENTATION                                  │
│    How Python's socket module, asyncio event loop, and OS kernel behave   │
│    (e.g., non-blocking I/O multiplexing via epoll/kqueue, SO_REUSEADDR,   │
│    GIL constraints on CPU-bound workloads, generator coroutine mechanics).│
├───────────────────────────────────────────────────────────────────────────┤
│ 3. OPERATIONAL & PRODUCTION REALITY                                       │
│    How systems fail and behave under real-world load                      │
│    (e.g., database connection pool exhaustion under traffic spikes,       │
│    cascading timeouts behind reverse proxies, thundering herd on caches, │
│    transaction deadlocks, poison-pill messages in queues).                │
└───────────────────────────────────────────────────────────────────────────┘
```
