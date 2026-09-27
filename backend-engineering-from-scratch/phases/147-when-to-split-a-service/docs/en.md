# Lesson 147: When to Split a Service

> **Motto**: Splitting a service is justified ONLY by differing scaling dimensions, independent deployment cycles, or organizational team ownership.

---

## Motto
"Splitting a service is justified ONLY by differing scaling dimensions, independent deployment cycles, or organizational team ownership."

## Problem
Splitting services because 'microservices are modern' introduces distributed failure modes without solving any business problem.

## Prediction
Evaluating concrete split criteria (scaling divergence, fault domain isolation, autonomous team velocity) justifies extractions.

## Why this matters
Splitting services is an organizational and operational tradeoff, never a graduation ceremony.

## First principles
Justified Split Drivers: 1. Independent Scaling (CPU-heavy vs I/O), 2. Team Autonomy (20+ devs), 3. Failure Domain Isolation.

## Mental model
```text
Evaluation: Is this module CPU-heavy while the rest is I/O? Do 15 engineers work exclusively on it? YES -> JUSTIFIED SPLIT.
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Microservice architectural trade-off evaluations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/147-when-to-split-a-service/tests/ -v
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
- **Failure Injection**: Run evaluation rubric against 3 scenarios: blog CRUD (Monolith), payment processing (Justified Split), image transcoding (Justified Split).
- Execute the experiment script:
```bash
python phases/147-when-to-split-a-service/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that simple CRUD fails the split threshold, while specialized compute or security domains pass.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never split a service if you don't have automated CI/CD, centralized logging, distributed tracing, and dedicated SRE support.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Data ownership must split when services split: a microservice must own its own private database.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Every network boundary you introduce converts a fast local function call into a fallible, slow network hop.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the three legitimate engineering justifications for extracting a microservice from a monolith?
2. Why is extracting microservices before establishing distributed tracing and CI/CD dangerous?
3. What happens to database joins and transactions when a module is extracted into a separate service?

## What comes next
Having understood when to split a service, we next discover its inherent boundaries and transition to **First Service Extraction**.
