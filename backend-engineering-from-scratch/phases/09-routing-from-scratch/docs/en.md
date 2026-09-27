# Lesson 09: Routing From Scratch

> **Motto**: A router is a lookup data structure mapping a (Method, Path) tuple to a callable execution handler.

---

## Motto
"A router is a lookup data structure mapping a (Method, Path) tuple to a callable execution handler."

## Problem
Engineers view @app.get('/users/{id}') as magic without understanding path matching algorithms.

## Prediction
Building a routing table with parameterized path matching exposes URL parsing and dispatch mechanics.

## Why this matters
Routing overhead directly affects request dispatch latency; complex regex routers can degrade performance.

## First principles
Routing is function lookup over a discrete search space defined by HTTP Method and URI path segments.

## Mental model
```text
(METHOD, PATH_TEMPLATE) -> Regex / Trie Match -> Path Variables Extracted -> Handler Executed
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI / Starlette APIRouter path dispatching and dependency tree resolution.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/09-routing-from-scratch/tests/ -v
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
- **Failure Injection**: Send request with duplicate route definition or mismatched HTTP method.
- Execute the experiment script:
```bash
python phases/09-routing-from-scratch/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Router detects method mismatch and returns HTTP 405 with Allow header; route not found returns 404.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Optimize router with radix tree / trie prefix matching for O(k) path lookup.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Path traversal: unvalidated path parameters used in filesystem lookups can leak arbitrary server files.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Route ordering matters in prefix-based routers; static routes must be registered before catch-all wildcards.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does a Trie-based router outperform naive linear list scanning?
2. Why should an unmatched path return 404, but a matched path with wrong method return 405?
3. How are URL path variables safely decoded and cast to domain types?

## What comes next
Having understood routing from scratch, we next discover its inherent boundaries and transition to **Introduce Web Framework**.
