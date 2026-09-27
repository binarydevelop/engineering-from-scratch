# Lesson Template

Use this template when authoring or reviewing any lesson in `backend-engineering-from-scratch`. Every lesson must follow this structure without omitting sections.

---

```markdown
# Lesson [NN]: [Lesson Title]

> **Motto**: [A single memorable sentence summarizing the foundational truth taught in this lesson.]

---

## Motto
"[Motto repeated here with immediate conceptual emphasis.]"

## Problem
[Explain the concrete problem that makes this mechanism necessary.
Show the pain of NOT having this mechanism. Do NOT start with framework abstractions.
Make the failure tangible.]

## Prediction
[State the exact empirical hypothesis.
What will happen when we send a specific byte sequence, request payload, or concurrent traffic?
The learner must predict before running.]

## Why this matters
[Explain the real-world operational consequence.
What outages, security breaches, data corruption, or latency spikes happen when an engineer misunderstands this layer?]

## First principles
[Derive the concept from fundamental truths:
- Sockets, operating system descriptors, and TCP byte streams
- Mathematical serialization and wire encodings
- Storage engines, ACID constraints, and isolation anomalies
- Concurrency limits, Little's Law, and backpressure
Avoid framework hand-waving.]

## Mental model
```text
[ASCII Diagram illustrating the exact data flow, memory transitions,
or network packet/request journey through the system]
```

## Build the simple version
[Implement the mechanism from scratch using Python standard library primitives:
- raw sockets
- minimal HTTP parser
- explicit dictionary routing
- manual SQL string parameterization
- hand-rolled middleware generator
- simple token bucket or mutex
Every code block must be fully runnable and self-contained.]

## Use the real tool/framework
[Now introduce the production-grade tool or framework abstraction (e.g. FastAPI, SQLAlchemy, Redis, Uvicorn, Bcrypt).
Directly map the handwritten mechanism to the framework construct.
Prove that the framework is NOT magic—it is merely convenience wrapped around the first-principles mechanism.]

## Test it
[Provide a pytest test suite verifying:
- Happy path execution
- Boundary conditions
- Malformed inputs
- Error status codes]

## Inspect it
[Directly observe the low-level state:
- Inspect raw bytes on the socket or wire
- Query the database system catalog or transaction status
- Inspect process file descriptors or memory structures
- Examine structured logs and header payloads]

## Measure it
[Quantify the behavior with concrete metrics:
- Latency (p50, p95, p99)
- Throughput (RPS)
- Memory RSS / garbage collection
- Database query count and execution time]

## Break it
[Inject an intentional failure:
- Send a malformed header or truncated body
- Trigger an unhandled exception or database constraint collision
- Induce a race condition with concurrent threads/tasks
- Exceed socket buffer or connection pool limits
Observe the exact breakdown.]

## Debug it
[Diagnose the failure using evidence:
- Check HTTP status code and response payload
- Read application stack traces and correlation IDs
- Inspect active database locks or connection pool states
- Trace the root cause to the failing layer]

## Improve it
[Refactor the implementation to eliminate the vulnerability, race, or performance bottleneck:
- Add connection timeouts and bounded retry limits
- Wrap operations in atomic transactions or optimistic locking
- Enforce strict input validation schemas
- Apply backpressure or rate limiting]

## Security
[Analyze the security perimeter:
- Attack vectors (injection, credential leakage, forgery, DoS)
- Defense-in-depth controls
- Data sanitization and principle of least privilege]

## Production implications
[Explain operational realities in real deployments:
- Cloud environments (AWS ALB/ECS, GCP Cloud Run)
- Container orchestration (Docker Compose, Kubernetes pods)
- Monitoring alerts and SLO budgets
- Zero-downtime rolling upgrades and database migrations]

## Evidence
[Instruct the learner to record their empirical findings in `outputs/evidence-template.md`.]

## Questions for mastery
1. [Mastery question probing deep mechanical understanding]
2. [Scenario-based question exploring an edge case or failure mode]
3. [Architecture question examining tradeoffs at scale]

## What comes next
[Preview the next lesson and show how the boundary of the current mechanism leads directly into the next architectural layer.]
```
