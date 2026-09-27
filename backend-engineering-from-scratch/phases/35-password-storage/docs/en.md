# Lesson 35: Password Storage

> **Motto**: Passwords must never be stored in plaintext or with fast cryptographic hashes; adaptive work-factor algorithms are mandatory.

---

## Motto
"Passwords must never be stored in plaintext or with fast cryptographic hashes; adaptive work-factor algorithms are mandatory."

## Problem
Storing passwords in MD5 or SHA-256 allows attackers to crack billions of passwords per second using commodity GPUs.

## Prediction
Hashing with bcrypt or Argon2id with unique cryptographic salts makes offline dictionary attacks computationally infeasible.

## Why this matters
Database leaks happen; modern password hashing ensures that a leaked database does not compromise user credentials.

## First principles
Hash = Algorithm(Password, Salt, WorkFactor). WorkFactor controls CPU and memory cost to hash.

## Mental model
```text
Plaintext Password + Cryptographic Salt -> Key Derivation Function (bcrypt/Argon2) -> Stored Hash String
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Passlib / Bcrypt password hashing utilities in production backends.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/35-password-storage/tests/ -v
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
- **Failure Injection**: Attempt to verify a password against an altered hash or empty password.
- Execute the experiment script:
```bash
python phases/35-password-storage/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that incorrect passwords return False without throwing unhandled exceptions.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Tune work factor to target ~250ms hashing time on production server CPUs.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never log plaintext passwords during registration, authentication, or debugging.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Increasing work factors over time protects against advancing GPU computation power.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why are fast hashing algorithms like SHA-256 dangerous for password storage?
2. What is the purpose of a unique cryptographic salt for every password?
3. How does the work factor parameter in bcrypt protect against offline brute-force attacks?

## What comes next
Having understood password storage, we next discover its inherent boundaries and transition to **Session-Based Authentication**.
