# Lesson 00: Backend Engineering Lab

> **Motto**: The backend is not an opaque cloud; it is operating system processes, network sockets, and state management that can be directly inspected.

---

## Motto
"The backend is not an opaque cloud; it is operating system processes, network sockets, and state management that can be directly inspected."

## Problem
Engineers treat backends as black boxes without knowing how to inspect the process, network sockets, or execution environment.

## Prediction
Running the environment checker will confirm Python 3.12+, socket binding, and local persistence capabilities.

## Why this matters
If you cannot verify your runtime and socket interfaces, you cannot isolate outages from environment misconfigurations.

## First principles
A backend begins as an operating system process holding an open file descriptor bound to a network port via the socket API.

## Mental model
```text
Source Code -> Python Process -> OS File Descriptor -> Listening Socket -> Client Connection
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI and Uvicorn server processes listening on TCP ports.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/00-backend-engineering-lab/tests/ -v
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
- **Failure Injection**: Port conflict: attempt binding to an already occupied port.
- Execute the experiment script:
```bash
python phases/00-backend-engineering-lab/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Check errno 48 (Address already in use); inspect active processes with lsof or ss.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use SO_REUSEADDR socket option and configure graceful port fallback.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never bind sensitive administrative sockets to 0.0.0.0; restrict to loopback 127.0.0.1 unless public ingress is intended.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Containerized pods bind to 0.0.0.0 inside container namespaces while host exposure is governed by Kubernetes Services / AWS ALBs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What operating system data structure represents a network socket?
2. What is the difference between binding to 127.0.0.1 and 0.0.0.0?
3. Why does SO_REUSEADDR prevent 'Address already in use' during rapid restarts?

## What comes next
Having understood backend engineering lab, we next discover its inherent boundaries and transition to **What Is a Backend?**.
