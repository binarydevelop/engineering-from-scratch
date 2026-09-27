# Lesson 112: Secrets

> **Motto**: Secrets are sensitive credentials (passwords, private keys, API tokens) that must never appear in source code or Git history.

---

## Motto
"Secrets are sensitive credentials (passwords, private keys, API tokens) that must never appear in source code or Git history."

## Problem
Accidentally committing database passwords or Stripe secret keys to GitHub leads to instant credential theft and automated bot exploits.

## Prediction
Injecting secrets dynamically from environment variables or external secret vaults (HashiCorp Vault, AWS Secrets Manager) protects credentials.

## Why this matters
Secret management hygiene prevents security breaches and allows zero-downtime credential rotation.

## First principles
Public Code Repository (Zero Secrets) <── Runtime Injection ──> Vault / Encrypted Environment Secrets.

## Mental model
```text
Developer Machine (Git: No Secrets) -> CI/CD -> Production Container receives secrets injected into memory at launch
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: AWS Secrets Manager and HashiCorp Vault client integration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/112-secrets/tests/ -v
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
- **Failure Injection**: Scan repository code with automated regex patterns to detect hardcoded API keys, JWT secrets, or private keys.
- Execute the experiment script:
```bash
python phases/112-secrets/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert scan detects zero committed secrets; verify secrets are loaded dynamically from environment variables.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce secret rotation: design backend authentication services to support key rotation without invalidating active sessions.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: If a secret is ever accidentally committed to Git, consider it immediately compromised: rotate the secret immediately.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Use tools like git-secrets, truffleHog, or GitHub Secret Scanning in pre-commit hooks and CI pipelines.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is committing secrets to private Git repositories still a major security vulnerability?
2. How do modern production backends inject secrets without storing them on container disk filesystems?
3. What operational steps must be taken immediately if an API secret key is committed to Git?

## What comes next
Having understood secrets, we next discover its inherent boundaries and transition to **12-Factor Concepts**.
