# Lesson 82: Backward Compatibility

> **Motto**: Backward compatibility guarantees that existing clients continue to function without modification when APIs evolve.

---

## Motto
"Backward compatibility guarantees that existing clients continue to function without modification when APIs evolve."

## Problem
Renaming or removing a JSON response field instantly crashes client parsers that expect the old field name.

## Prediction
Making all evolutions additive (adding new optional fields, never removing or renaming) preserves client stability.

## Why this matters
Understanding backward compatibility rules allows engineering teams to ship updates continuously without breaking users.

## First principles
Additive Changes (Safe): Adding a field. Subtractive Changes (Breaking): Removing a field, changing a type.

## Mental model
```text
Old Contract: {id, name} -> Safe Evolution: {id, name, email} -> Breaking Evolution: {id, full_name}
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pydantic schema inheritance with deprecation aliases.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/82-backward-compatibility/tests/ -v
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
- **Failure Injection**: Attempt to deploy an API modification that renames an existing field; schema validator flags breaking change.
- Execute the experiment script:
```bash
python phases/82-backward-compatibility/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Apply alias backward compatibility: support both old and new field names simultaneously during transition.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Postel's Law (Robustness Principle): 'Be conservative in what you send, be liberal in what you accept.'
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Breaking changes require a phased migration: 1. Add new field -> 2. Deprecate old -> 3. Migrate clients -> 4. Remove old.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Run contract testing in CI pipelines to automatically block pull requests that introduce breaking changes.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between an additive change and a breaking contract change?
2. How does Postel's Law guide robust API design and serialization?
3. What four-stage migration strategy is required to safely rename an existing API field in production?

## What comes next
Having understood backward compatibility, we next discover its inherent boundaries and transition to **OpenAPI**.
