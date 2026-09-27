# Lesson 153: Feature Flags

> **Motto**: Feature flags decouple code deployment from feature release, enabling safe runtime toggling and canary testing.

---

## Motto
"Feature flags decouple code deployment from feature release, enabling safe runtime toggling and canary testing."

## Problem
Deploying code directly to 100% of users means any hidden bug instantly impacts all customers simultaneously.

## Prediction
Wrapping new features in feature flags allows enabling features for internal employees first, rolling back instantly if errors spike.

## Why this matters
Feature flags enable trunk-based development, eliminate long-lived feature branches, and de-risk deployments.

## First principles
Code Deploy (Inactive Flag) -> Enable Flag for 1% of Users -> Monitor Error Rates -> Roll Out to 100% or Disable Instantly.

## Mental model
```text
if feature_flags.is_enabled('new_checkout', user_id):
    return execute_new_checkout()
return execute_legacy_checkout()
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: LaunchDarkly and Unleash feature flag patterns in Python backends.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/153-feature-flags/tests/ -v
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
- **Failure Injection**: Toggle a feature flag from False to True at runtime; verify endpoint immediately switches behavior without redeploying code.
- Execute the experiment script:
```bash
python phases/153-feature-flags/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Simulate an error spike on the new feature; toggle flag to False; verify endpoint instantly reverts to legacy behavior.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Clean up stale feature flags: dead feature flag checks left in code create massive technical debt and confusing logic paths.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Feature flag evaluations must be blazing fast (in-memory evaluation with periodic background sync); never query SQL on every check.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Ensure feature flag states are recorded in telemetry spans to correlate error spikes with specific flag rollouts.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How do feature flags decouple the act of deploying code from the act of releasing a feature to users?
2. What operational risk arises when engineering teams fail to remove stale feature flags from codebases?
3. Why must feature flag evaluation be performed in local process memory rather than querying a remote database on every request?

## What comes next
Having understood feature flags, we next discover its inherent boundaries and transition to **Canary / Gradual Rollout Concepts**.
