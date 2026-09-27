# Lesson 114: Graceful Shutdown

> **Motto**: Graceful shutdown allows in-flight requests to complete and safely closes open connections when a process receives SIGTERM.

---

## Motto
"Graceful shutdown allows in-flight requests to complete and safely closes open connections when a process receives SIGTERM."

## Problem
Killing a web server instantly (`SIGKILL`) cuts off active customer transactions, drops in-flight database writes, and corrupts state.

## Prediction
Intercepting `SIGTERM`, stopping new connection acceptance, and waiting for active requests to finish ensures zero dropped requests.

## Why this matters
Graceful shutdown is essential for seamless rolling deployments in Kubernetes, AWS ECS, and Docker environments.

## First principles
SIGTERM Received -> Stop Accepting New Connections -> Allow 15s for In-Flight Requests to Finish -> Close Pools -> Exit 0.

## Mental model
```text
Orchestrator sends SIGTERM ──> 1. Drain Traffic ──> 2. Complete Active Requests ──> 3. Close DB/Redis Pools ──> Exit Cleanly
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Uvicorn / FastAPI lifespan context managers and graceful shutdown handlers.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/114-graceful-shutdown/tests/ -v
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
- **Failure Injection**: Send SIGTERM to the process while an HTTP request is actively sleeping for 2 seconds.
- Execute the experiment script:
```bash
python phases/114-graceful-shutdown/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe process refuses new requests, waits for the active request to finish successfully (200 OK), closes DB pool, and exits.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Configure a maximum termination grace period (e.g. 30 seconds); force exit if requests hang beyond the timeout.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Kubernetes sends `SIGTERM`, waits `terminationGracePeriodSeconds` (default 30s), then sends `SIGKILL` if still running.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Always close database connection pools and queue consumers during shutdown to avoid leaving orphaned backend sessions.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the operational difference between SIGTERM (polite termination) and SIGKILL (instant kill)?
2. What sequence of actions must a web backend execute upon receiving a SIGTERM signal?
3. What happens if an in-flight database transaction is cut off by a hard process termination?

## What comes next
Having understood graceful shutdown, we next discover its inherent boundaries and transition to **Process Model**.
