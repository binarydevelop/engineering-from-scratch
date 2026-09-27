# Lesson 111: Configuration

> **Motto**: Application configuration varies across environments (dev, test, prod) and must be separated strictly from executable code.

---

## Motto
"Application configuration varies across environments (dev, test, prod) and must be separated strictly from executable code."

## Problem
Hardcoding database connection strings, API URLs, and ports inside source code requires recompiling and redeploying to change environments.

## Prediction
Loading configuration from environment variables and validating it at startup guarantees portable, 12-factor application builds.

## Why this matters
Validated configuration catches missing environment variables and misconfigured ports at boot time, preventing runtime crashes.

## First principles
Code is constant; Config varies. Inject config via Environment Variables (`DATABASE_URL`, `PORT`, `LOG_LEVEL`).

## Mental model
```text
OS Environment Variables -> Pydantic BaseSettings -> Validation (Types/URLs) -> Typed App Settings Object
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pydantic Settings (`BaseSettings`) and `.env` file management.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/111-configuration/tests/ -v
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
- **Failure Injection**: Attempt to start application with a missing mandatory `DATABASE_URL` or an invalid port integer.
- Execute the experiment script:
```bash
python phases/111-configuration/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Application fails fast at boot with a clear validation error detailing missing configuration, refusing to start corrupted.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never commit `.env` files containing environment-specific values to version control; commit `.env.example` as a template.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Validate environment variable types (ports are integers 1-65535, URLs are valid) to prevent subtle runtime type errors.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: In Kubernetes/AWS environments, configuration is injected into container environments via ConfigMaps or Parameter Store.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does the 12-Factor App methodology require strict separation of configuration from code?
2. Why should an application validate all configuration at process startup and fail fast if invalid?
3. What is the role of `.env.example` in a backend repository?

## What comes next
Having understood configuration, we next discover its inherent boundaries and transition to **Secrets**.
