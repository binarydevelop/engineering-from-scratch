# Lesson 102: Property and Edge-Case Testing

> **Motto**: Property-based testing generates hundreds of pseudo-random inputs to discover edge cases that human developers overlook.

---

## Motto
"Property-based testing generates hundreds of pseudo-random inputs to discover edge cases that human developers overlook."

## Problem
Handcrafted test cases only test scenarios the developer anticipated, leaving boundary edge cases undiscovered.

## Prediction
Defining mathematical properties (e.g. `deserialize(serialize(x)) == x`) and generating extreme inputs finds subtle bugs.

## Why this matters
Property testing uncovers integer overflows, unicode normalization bugs, empty string crashes, and rounding errors.

## First principles
Property: For ALL valid inputs $X$, invariant $P(X)$ must hold. Generator tests 1,000 randomized variations.

## Mental model
```text
Hypothesis Generator -> Generates: Negative numbers, Max Int, Emoji strings, Null bytes -> Tests Invariant -> Finds Failure!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Hypothesis library integration in Python backend testing.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/102-property-and-edge-case-testing/tests/ -v
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
- **Failure Injection**: Run property tests on an order discount calculation function across random price, quantity, and discount inputs.
- Execute the experiment script:
```bash
python phases/102-property-and-edge-case-testing/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Test generator finds a combination (e.g. fractional cents rounding bug) where total becomes negative; fix invariant.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Property testing is essential for financial arithmetic, parser boundaries, and pagination cursors.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: When property testing finds a bug, it 'shrinks' the input to the minimal reproducible example.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Combine property tests with fuzz testing on public API boundary deserializers to find parser crashes.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does property-based testing differ from standard example-based testing?
2. What is 'input shrinking' in property-based testing libraries like Hypothesis?
3. What types of backend calculations (e.g. financial, pagination) benefit most from property testing?

## What comes next
Having understood property and edge-case testing, we next discover its inherent boundaries and transition to **Load Testing**.
