# Lesson 119: Containerize Backend

> **Motto**: Containers package application code, system libraries, and runtime dependencies into immutable, reproducible execution images.

---

## Motto
"Containers package application code, system libraries, and runtime dependencies into immutable, reproducible execution images."

## Problem
Deploying directly to virtual machines causes environment drift ('it worked on my laptop but broke on production Ubuntu').

## Prediction
Writing a multi-stage Dockerfile produces lightweight, secure container images that run identically anywhere Docker is installed.

## Why this matters
Containers are the standard deployment unit for modern backend engineering, Kubernetes, and cloud platforms.

## First principles
Source Code + Dockerfile -> Docker Build -> Immutable Container Image -> Docker Run -> Isolated Container Process.

## Mental model
```text
Build Stage (Compiles deps, tools) -> Production Stage (Copies compiled wheels, runs as unprivileged user, tiny image)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Docker CLI and container runtime commands (`docker build`, `docker run`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/119-containerize-backend/tests/ -v
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
- **Failure Injection**: Build the multi-stage Docker container image; verify image size is < 150MB and runs as a non-root user.
- Execute the experiment script:
```bash
python phases/119-containerize-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Execute health check inside running container; verify application starts and responds to HTTP requests.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never run container processes as `root`: create a dedicated unprivileged user (`USER appuser`) to mitigate container breakout attacks.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Use `.dockerignore` to exclude virtualenvs, Git directories, `.env` files, and test caches from image builds.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Pin base image tags explicitly (`python:3.12-slim-bookworm`); never use floating `latest` tags in production.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why are multi-stage Docker builds used when packaging backend applications?
2. Why is running container processes as the `root` user a critical security hazard?
3. What files should always be excluded in a `.dockerignore` file?

## What comes next
Having understood containerize backend, we next discover its inherent boundaries and transition to **Docker Compose Stack**.
