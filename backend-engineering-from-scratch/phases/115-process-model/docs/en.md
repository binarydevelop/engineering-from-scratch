# Lesson 115: Process Model

> **Motto**: A production process model runs multiple independent worker processes to utilize multi-core CPUs and isolate failures.

---

## Motto
"A production process model runs multiple independent worker processes to utilize multi-core CPUs and isolate failures."

## Problem
A single Python process only utilizes a single CPU core, leaving modern multi-core servers 80-90% unutilized.

## Prediction
Running a master process that manages multiple worker processes (Gunicorn/Uvicorn workers) scales throughput linearly with CPU cores.

## Why this matters
Worker processes have isolated memory spaces; a crash or memory leak in one worker does not affect the others.

## First principles
Master Process (Supervises, handles signals) -> Spawns N Workers (one per CPU core) -> Workers accept requests on shared socket.

## Mental model
```text
Master Process (PID 100) ──┬──> Worker 1 (PID 101) [Core 1]
                           ├──> Worker 2 (PID 102) [Core 2]
                           └──> Worker 3 (PID 103) [Core 3]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Gunicorn multi-worker management (`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/115-process-model/tests/ -v
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
- **Failure Injection**: Kill a child worker process with `kill -9`; observe master supervisor detects exit and spawns a fresh replacement worker immediately.
- Execute the experiment script:
```bash
python phases/115-process-model/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify service remains available throughout worker crash; active requests on other workers are unaffected.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Because worker processes have separate memory, in-memory caches or variables are NOT shared across workers.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Formula for sizing web workers: $\text{Workers} = (2 \times \text{CPU Cores}) + 1$ for sync, or $1 \times \text{Cores}$ for async.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Master process listens on the network socket with `SO_REUSEPORT`, allowing the OS kernel to balance incoming connections across workers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does a single Python backend process fail to utilize multiple CPU cores?
2. What happens to in-memory state (like a Python dictionary cache) when running across 4 worker processes?
3. How does a master process detect when a worker process has crashed and recover?

## What comes next
Having understood process model, we next discover its inherent boundaries and transition to **Reverse Proxy**.
