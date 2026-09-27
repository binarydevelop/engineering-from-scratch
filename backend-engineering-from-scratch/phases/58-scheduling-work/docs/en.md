# Lesson 58: Scheduling Work

> **Motto**: Scheduled work triggers recurring jobs at predetermined intervals or calendar times for maintenance and reporting.

---

## Motto
"Scheduled work triggers recurring jobs at predetermined intervals or calendar times for maintenance and reporting."

## Problem
Running recurring jobs via ad-hoc sleep loops inside web processes causes duplicate executions across replicas.

## Prediction
Centralized scheduling (cron, queue scheduler, Celery Beat) guarantees tasks run predictably on schedule.

## Why this matters
Scheduled jobs power essential business workflows: daily invoice generation, data archiving, and cache pre-warming.

## First principles
Scheduler Process -> Evaluates Cron Expressions -> Enqueues Task into Durable Queue -> Workers Consume.

## Mental model
```text
Cron Trigger ('0 0 * * *') -> Scheduler enqueues DailySummaryJob -> Worker picks up and runs job
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Celery Beat / APScheduler recurring task orchestration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/58-scheduling-work/tests/ -v
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
- **Failure Injection**: Run two application replicas with an uncoordinated scheduler; observe duplicate job execution.
- Execute the experiment script:
```bash
python phases/58-scheduling-work/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Introduce distributed leader election or centralized queue scheduler; observe exactly one job runs on schedule.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Ensure scheduled jobs are idempotent; a delayed or re-run scheduled job must not double-count metrics.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Long-running scheduled jobs should be chunked into batches to prevent locking database tables during peak hours.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Monitor scheduler heartbeat; if the scheduler process dies, recurring business tasks silently stop running.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does running recurring tasks inside web application processes fail when scaling to multiple replicas?
2. What is the role of a distributed lock (e.g. Redlock) in recurring job schedulers?
3. How should large batch maintenance jobs be scheduled to avoid degrading active user traffic?

## What comes next
Having understood scheduling work, we next discover its inherent boundaries and transition to **Events vs Commands**.
