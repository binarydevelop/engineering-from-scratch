# Lesson 168: Debugging Lab: Disk Full

> **Motto**: Diagnosing database and application crashes caused by unrotated log files filling server disks requires disk auditing.

---

## Motto
"Diagnosing database and application crashes caused by unrotated log files filling server disks requires disk auditing."

## Problem
A database suddenly crashes and refuses to start; application writes fail with `IOError: [Errno 28] No space left on device`.

## Prediction
Using `df -h` and `du -sh *` locates massive unrotated log files or runaway temporary file directories.

## Why this matters
Configuring log rotation (`logrotate`) and disk monitoring alerts prevents catastrophic disk exhaustion outages.

## First principles
Application writes 100GB of unrotated logs to `/var/log` -> Disk reaches 100% -> PostgreSQL cannot write WAL -> CRASH.

## Mental model
```text
Disk Usage: 99% -> 100% -> Database WAL write fails -> Database enters read-only emergency recovery -> API down!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Linux disk management and Docker log rotation configurations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/168-debugging-lab-disk-full/tests/ -v
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
- **Failure Injection**: Simulate disk fill by generating an oversized unrotated log file; attempt database write; observe failure.
- Execute the experiment script:
```bash
python phases/168-debugging-lab-disk-full/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Run `df -h` and `du` to locate oversized log file; truncate log file; restore database operations; configure log rotation.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Configure Docker log rotation in `daemon.json`: set `max-size: '50m'` and `max-file: '3'` to cap container logs.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: When disk space reaches 100%, relational databases shut down or enter read-only mode to prevent database file corruption.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Set monitoring alerts on disk utilization at 80% (Warning) and 90% (Critical) to provide time for remediation.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What happens to a relational database like PostgreSQL when the underlying disk filesystem reaches 100% capacity?
2. What Linux command utilities are used to identify which directories and files are consuming disk space?
3. How does configuring Docker daemon log rotation prevent container logs from consuming the entire host disk?

## What comes next
Having understood debugging lab: disk full, we next discover its inherent boundaries and transition to **Debugging Lab: DNS Failure**.
