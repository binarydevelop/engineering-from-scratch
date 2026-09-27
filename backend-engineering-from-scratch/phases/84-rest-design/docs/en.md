# Lesson 84: REST Design

> **Motto**: REST is an architectural style utilizing standard HTTP methods, resource URIs, and representations for uniform interfaces.

---

## Motto
"REST is an architectural style utilizing standard HTTP methods, resource URIs, and representations for uniform interfaces."

## Problem
Creating chaotic RPC URLs like `/do_update_user_name_and_status` makes APIs inconsistent and impossible to navigate.

## Prediction
Modeling business domains as resources (`/users/{id}`, `/orders/{id}/items`) creates intuitive, predictable APIs.

## Why this matters
Adhering to pragmatic REST principles makes APIs easy to learn, cacheable at the HTTP layer, and standard.

## First principles
Resources (Nouns) + Standard Methods (Verbs) + Representation (JSON) + Status Codes (Outcome).

## Mental model
```text
Collection Resource: `/orders` (GET: list, POST: create) | Instance Resource: `/orders/42` (GET: read, DELETE: remove)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI resource routing adhering to REST principles.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/84-rest-design/tests/ -v
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
- **Failure Injection**: Send non-standard method requests or verbs in URLs; observe architectural refactoring to clean resource URIs.
- Execute the experiment script:
```bash
python phases/84-rest-design/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify uniform status codes and resource representation structures across all endpoints.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Avoid dogmatic 'REST purity' (e.g. strict HATEOAS) when it complicates practical client consumption without benefit.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Sub-resources: nest resources only one level deep (`/users/{id}/orders`); avoid deep nesting (`/a/1/b/2/c/3/d/4`).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: For non-CRUD operations, model the action as a sub-resource or state transition (`POST /orders/{id}/cancellation`).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why are nouns preferred over verbs for RESTful URL paths?
2. Why is deep nesting of resources (e.g. `/authors/1/books/2/chapters/3/comments/4`) considered an anti-pattern?
3. How should complex business operations that do not map to simple CRUD be modeled in REST?

## What comes next
Having understood rest design, we next discover its inherent boundaries and transition to **RPC / gRPC Concepts**.
