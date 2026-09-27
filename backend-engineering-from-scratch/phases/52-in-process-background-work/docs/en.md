# Lesson 52: In-Process Background Work

> **Motto**: In-process background tasks execute asynchronously within the application runtime, but lack durability across process restarts.

---

## Motto
"In-process background tasks execute asynchronously within the application runtime, but lack durability across process restarts."

## Problem
Teams use in-process tasks for critical financial operations, losing transactions whenever deployments or crashes occur.

## Prediction
Understanding `asyncio.create_task` and framework background workers defines when simple tasks suffice vs durable queues.

## Why this matters
In-process tasks are lightweight and require no external infrastructure, making them ideal for non-critical telemetry.

## First principles
Async Event Loop -> Spawn Task (in-memory) -> Returns response immediately -> Loop executes task when I/O yields.

## Mental model
```text
HTTP Handler -> asyncio.create_task(log_event()) -> Response returned -> Background Task completes in event loop
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI `BackgroundTasks` parameter in route functions.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/52-in-process-background-work/tests/ -v
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
- **Failure Injection**: Trigger an in-process background task and immediately terminate the Python process.
- Execute the experiment script:
```bash
python phases/52-in-process-background-work/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe that the background task is terminated midway and never finishes; state is lost.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Only use in-process tasks for ephemeral, non-critical operations (audit logs, cache warming, fire-and-forget metrics).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unhandled exceptions in background tasks can crash event loops or go completely unnoticed without error handlers.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: During rolling deployments, new containers terminate old containers, killing all in-flight in-process background work.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What happens to an asyncio background task when the host process is terminated by Docker during a deploy?
2. What types of tasks are safe for in-process background execution, and which require durable queues?
3. How do you capture and log unhandled exceptions occurring inside background tasks?

## What comes next
Having understood in-process background work, we next discover its inherent boundaries and transition to **Durable Queue**.
