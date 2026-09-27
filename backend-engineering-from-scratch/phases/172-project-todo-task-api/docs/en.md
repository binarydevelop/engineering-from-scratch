# Lesson 172: Project: Todo / Task API

> **Motto**: Build a clean architecture Task Management API with authentication, ownership authorization, pagination, and full test coverage.

---

## Motto
"Build a clean architecture Task Management API with authentication, ownership authorization, pagination, and full test coverage."

## Problem
Simple CRUD is often built as unstructured spaghetti; building it with clean architecture creates a reusable production template.

## Prediction
Structuring entities, repositories, use-case services, and controllers demonstrates professional software engineering discipline.

## Why this matters
This project serves as the clean architecture blueprint for all standard enterprise REST APIs.

## First principles
Controller -> TaskService -> TaskRepository -> SQL. Authentication middleware injects verified user context.

## Mental model
```text
Clean Layers: HTTP Controller (FastAPI) -> Application Service -> Domain Entity -> Repository Interface -> SQL Database
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Clean Architecture reference application.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/172-project-todo-task-api/tests/ -v
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
- **Failure Injection**: Execute full test suite covering user registration, task creation, ownership isolation, filtering, and pagination.
- Execute the experiment script:
```bash
python phases/172-project-todo-task-api/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that User B receives HTTP 404 when attempting to access a task owned by User A.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep domain entities pure: business rules (e.g. 'Completed tasks cannot be edited') belong in domain models.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Expose structured error responses following RFC 9457 Problem Details.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Structure repository methods to accept pagination and filter criteria objects rather than raw SQL parameters.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Clean Architecture separate transport controllers from database persistence?
2. How is resource ownership authorization enforced across task CRUD operations?
3. Why does a properly structured Task API serve as a reference template for enterprise backend development?

## What comes next
Having understood project: todo / task api, we next discover its inherent boundaries and transition to **Project: Blog Platform**.
