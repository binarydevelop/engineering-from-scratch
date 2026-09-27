# Lesson 120: Docker Compose Stack

> **Motto**: Docker Compose coordinates multi-container environments, defining networking, volumes, and health dependencies across services.

---

## Motto
"Docker Compose coordinates multi-container environments, defining networking, volumes, and health dependencies across services."

## Problem
Running a multi-service backend requires manually starting Postgres, Redis, the Web API, and background workers in the right order.

## Prediction
A `docker-compose.yml` file defines the entire architecture as code, allowing developers to spin up the full stack with one command.

## Why this matters
Docker Compose provides production parity on local developer laptops, ensuring seamless team onboarding and testing.

## First principles
Compose File -> Defines: Services (API, DB, Redis, Worker) + Networks (Internal bridge) + Volumes (Persistent storage).

## Mental model
```text
docker compose up ──┬──> PostgreSQL Container (Healthy)
                     ├──> Redis Container (Healthy)
                     ├──> Web API Container (Depends on DB & Redis)
                     └──> Worker Container (Consumes from Redis)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Docker Compose orchestration commands (`docker compose up`, `docker compose ps`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/120-docker-compose-application-stack/tests/ -v
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
- **Failure Injection**: Run `docker compose config` to validate compose file syntax, networking topology, and environment variable bindings.
- Execute the experiment script:
```bash
python phases/120-docker-compose-application-stack/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify service dependency graph: ensure web API and worker containers declare `depends_on` with `condition: service_healthy`.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always use named Docker volumes for databases (`pgdata:/var/lib/postgresql/data`) to prevent data loss when containers stop.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never expose internal database and Redis ports to the public Internet; keep them on isolated Docker internal bridge networks.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Use environment files (`env_file: .env`) to inject configuration without hardcoding passwords in compose manifests.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should service dependencies use `condition: service_healthy` rather than simple `depends_on`?
2. What is the purpose of named Docker volumes for database containers?
3. How do Docker bridge networks provide network isolation between multi-tier services?

## What comes next
Having understood docker compose stack, we next discover its inherent boundaries and transition to **Database Startup / Dependency Failure**.
