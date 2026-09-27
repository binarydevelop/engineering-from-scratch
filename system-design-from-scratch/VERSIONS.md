# Software Versions and Toolchain Baselines

This document records the exact runtime environment and dependency versions verified for `system-design-from-scratch`.
Every version was tested and validated on macOS (Darwin arm64/x86_64) and Linux (Ubuntu 22.04 LTS / Debian 12).

---

## 1. Primary Language Runtime

| Component | Verified Version | Minimum Required | Purpose / Notes |
| :--- | :--- | :--- | :--- |
| **Python** | `3.12.14` | `3.12.0+` | Primary language for simulation models, mathematical estimates, failure harnesses, and distributed prototypes. Employs modern syntax, improved error tracebacks, and enhanced `asyncio` performance. |

---

## 2. Frameworks and Application Libraries

| Package | Verified Version | Purpose in Curriculum |
| :--- | :--- | :--- |
| **`pytest`** | `9.1.1` | Automated test runner verifying system invariants, chaos tests, and algorithmic simulators. |
| **`httpx`** | `0.28.1` | High-throughput asynchronous HTTP client used in load test harnesses and gateway simulations. |
| **`fastapi`** | `0.141.1` | Modern, high-performance web framework used for API gateway and microservice prototype endpoints. |
| **`uvicorn`** | `0.53.0` | Production-grade ASGI server implementation based on `uvloop` and `httptools`. |
| **`pydantic`** | `2.13.5` | High-speed data parsing, schema validation, and serialization with Rust core. |
| **`cryptography`** | `50.0.1` | Cryptographic primitives for tokens, hash rings, and signature validation. |
| **`pyjwt`** | `2.15.0` | RFC 7519 JSON Web Token issuance and signature verification. |
| **`anyio`** | `4.15.1` | Asynchronous structured concurrency library supporting both `asyncio` and `trio`. |

---

## 3. Infrastructure & Operating System Primitives

| Tool | Verified Version | Role in System Design |
| :--- | :--- | :--- |
| **`curl`** | `8.7.1` | Raw HTTP wire inspection and manual gateway probing. |
| **`sqlite3`** | `3.43.2+` | Embedded relational engine used for local persistence and ACID transaction simulations. |
| **`git`** | `2.54.0+` | Version control and reproducibility. |
| **`make`** | `GNU Make 3.81+` | Automation command center for running tests, simulations, and benchmarks. |
| **`docker`** | `29.7.2+` *(Optional)* | Containerization of multi-node cluster topologies. |

---

## 4. Verification Command

Verify your local environment against these pinned versions:
```bash
make env-check
```
