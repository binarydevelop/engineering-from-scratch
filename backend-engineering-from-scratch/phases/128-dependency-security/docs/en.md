# Lesson 128: Dependency Security

> **Motto**: Third-party libraries introduce external code into your runtime; dependency security audits detect known vulnerabilities (CVEs).

---

## Motto
"Third-party libraries introduce external code into your runtime; dependency security audits detect known vulnerabilities (CVEs)."

## Problem
Using outdated Python packages with unpatched vulnerabilities allows automated attackers to exploit known remote code execution bugs.

## Prediction
Pinning exact dependency hashes and scanning with `pip-audit` prevents supply chain attacks and known CVE exploits.

## Why this matters
Dependency security ensures that your application code is not compromised by vulnerabilities in upstream packages.

## First principles
Dependency Tree: Direct dependencies + Transitive dependencies. Vulnerability in any sub-dependency compromises application.

## Mental model
```text
requirements.txt / lockfile ──[pip-audit / safety]──> Query Vulnerability Database (CVE) ──> Pass / Alert on Vuln
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pip-audit and safety CLI tooling in Python pipelines.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/128-dependency-security/tests/ -v
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
- **Failure Injection**: Scan an intentionally outdated package list containing a known vulnerable package; verify auditor flags the CVE and CVSS score.
- Execute the experiment script:
```bash
python phases/128-dependency-security/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Update the package to the patched version; re-run audit; assert zero vulnerabilities detected.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always pin exact versions in `requirements.txt` or use lockfiles (`uv.lock`, `poetry.lock`) to ensure reproducible builds.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Supply chain attacks: verify package authenticity using cryptographic package hashes (`--require-hashes`).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Automate weekly dependency vulnerability scans in CI even when no code changes are committed.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is a Common Vulnerabilities and Exposures (CVE) identifier and CVSS score?
2. What is a transitive dependency vulnerability and why is it difficult to detect manually?
3. How do dependency lockfiles protect against supply chain attacks?

## What comes next
Having understood dependency security, we next discover its inherent boundaries and transition to **Input Size Limits**.
