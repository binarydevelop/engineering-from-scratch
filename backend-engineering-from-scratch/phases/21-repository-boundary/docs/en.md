# Lesson 21: Repository Boundary

> **Motto**: A repository mediates between the domain layer and data mapping using a collection-like interface for domain entities.

---

## Motto
"A repository mediates between the domain layer and data mapping using a collection-like interface for domain entities."

## Problem
Scattering raw SQL queries across route handlers creates duplicate logic, tight coupling, and untestable code.

## Prediction
Encapsulating SQL queries behind a repository interface isolates SQL syntax and schema details from use-cases.

## Why this matters
Repositories allow switching persistence mechanisms or swapping mock repositories in tests with zero use-case changes.

## First principles
The repository is an explicit boundary translating database rows (relational) into domain entities (object/graph).

## Mental model
```text
Application Service -> Repository Interface (get_by_id, save) -> Concrete SQL Repository -> Relational Database
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Repository pattern integrated with dependency injection in a FastAPI service.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/21-repository-boundary/tests/ -v
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
- **Failure Injection**: Modify an underlying database table column name; observe that only the repository implementation changes.
- Execute the experiment script:
```bash
python phases/21-repository-boundary/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that application services and route handlers remain completely untouched by schema changes.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce strict domain entity return types; never return raw database cursor dictionaries from repositories.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Prevent SQL injection by keeping all parameterization encapsulated strictly within the repository layer.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Repositories should model domain aggregates, not 1:1 mirrors of raw database tables.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between an Active Record pattern and a Repository pattern?
2. Why should a repository return a domain entity instead of a raw SQL row dictionary?
3. How does a repository interface simplify unit testing?

## What comes next
Having understood repository boundary, we next discover its inherent boundaries and transition to **CRUD Correctly**.
