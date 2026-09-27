# Lesson 151: API Gateway Concept

> **Motto**: An API Gateway provides a single, unified entry point for clients, routing requests to internal microservices and handling cross-cutting concerns.

---

## Motto
"An API Gateway provides a single, unified entry point for clients, routing requests to internal microservices and handling cross-cutting concerns."

## Problem
Forcing mobile clients to call 15 different microservices directly exposes internal architecture, leaks IPs, and requires complex client auth.

## Prediction
An API Gateway centralizes authentication, SSL termination, rate limiting, request routing, and protocol translation.

## Why this matters
Gateways decouple public API contracts from private, evolving internal microservice topologies.

## First principles
Clients (Mobile/Web) ──[HTTPS]──> API Gateway ──┬──> User Service (Private VPC)
                                                ├──> Order Service (Private VPC)
                                                └──> Catalog Service (Private VPC)

## Mental model
```text
Client -> GET /api/v1/orders -> API Gateway (AuthN, Rate Limit) -> Routes to internal `http://orders-svc:8080/orders`
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Kong, Traefik, and FastAPI API Gateway implementations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/151-api-gateway-concept/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Send an unauthenticated request to the Gateway; verify the Gateway rejects with HTTP 401 before hitting internal services.
- Execute the experiment script:
```bash
python phases/151-api-gateway-concept/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Send a valid request; verify Gateway injects `X-User-ID` and `X-Tenant-ID` headers and routes to the correct internal service.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep the API Gateway lightweight: never put complex business logic or database access inside an API gateway.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Avoid making the API Gateway a development bottleneck where every team must modify gateway code to ship features.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Gateways can perform response aggregation (Backend For Frontend pattern) to reduce mobile network roundtrips.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What architectural responsibilities belong in an API Gateway versus downstream microservices?
2. Why should complex business logic never be implemented inside an API Gateway?
3. How does an API Gateway protect internal microservices from being directly exposed to the public Internet?

## What comes next
Having understood api gateway concept, we next discover its inherent boundaries and transition to **Backend for Frontend Concept**.
