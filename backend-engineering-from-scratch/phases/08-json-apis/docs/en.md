# Lesson 08: JSON APIs

> **Motto**: Wire representation is not domain state; an API must serialize and deserialize JSON with defensive type boundaries.

---

## Motto
"Wire representation is not domain state; an API must serialize and deserialize JSON with defensive type boundaries."

## Problem
Treating incoming JSON as trusted Python dictionaries leads to KeyError crashes and injection vulnerabilities.

## Prediction
Validating JSON structure before execution prevents unhandled exceptions deep in business logic.

## Why this matters
JSON serialization is a CPU and memory bottleneck at high throughput; understanding the cost matters.

## First principles
JSON (RFC 8259) is text serialization; domain objects possess behavior, types, and invariants.

## Mental model
```text
Wire Bytes -> Unicode Decode -> JSON Parse (dict/list) -> Domain Validation -> Typed Entity
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pydantic BaseModel deserialization and JSON serialization in FastAPI.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/08-json-apis/tests/ -v
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
- **Failure Injection**: Submit invalid JSON (trailing comma, unquoted key, NaN) or incorrect primitive types.
- Execute the experiment script:
```bash
python phases/08-json-apis/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Parser traps JSONDecodeError and returns clean HTTP 400 with character offset.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Add recursive depth limits and payload size guards to prevent parser DoS.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: JSON parsing is vulnerable to Hash Collision DoS and deeply nested object stack overflows.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: High-throughput microservices often profile JSON serialization costs and consider orjson or binary formats.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is raw json.loads() insufficient for API boundary validation?
2. How does recursive JSON nesting cause stack exhaustion?
3. What is the difference between serialization and domain mapping?

## What comes next
Having understood json apis, we next discover its inherent boundaries and transition to **Routing From Scratch**.
