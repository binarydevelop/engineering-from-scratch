# Lesson 106: Application Profiling

> **Motto**: Application profiling identifies exact CPU hotspots, function call counts, and memory allocations in Python code.

---

## Motto
"Application profiling identifies exact CPU hotspots, function call counts, and memory allocations in Python code."

## Problem
Guessing where an application spends its time is notoriously inaccurate; profiling with cProfile reveals actual bottlenecks.

## Prediction
Instrumenting code with profilers exposes slow regexes, redundant JSON deserializations, and unnecessary loops.

## Why this matters
Profiling guides targeted, high-impact optimizations, turning 200ms Python endpoints into 5ms endpoints.

## First principles
Profiler hooks into Python interpreter execution: records function entries, exits, call counts, and cumulative execution time.

## Mental model
```text
cProfile Output: Function Name | Number of Calls | Total Time | Cumulative Time -> Pinpoints exact slow function
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Python `cProfile` standard library module and snakeviz visualization.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/106-application-profiling/tests/ -v
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
- **Failure Injection**: Profile an endpoint executing an unoptimized nested loop and repetitive regex compilation.
- Execute the experiment script:
```bash
python phases/106-application-profiling/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Profiler output instantly flags `re.compile()` inside a loop consuming 85% of total request execution time.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Refactor: compile regex once at module startup; re-profile; observe CPU execution duration drops by 80%.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Profiling in production: continuous profiling (py-spy) samples call stacks with minimal (< 1%) overhead.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Do not optimize code that accounts for < 2% of total request time; focus on the top 3 hotspots.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What information does `cProfile` provide that simple start/end timestamp logging cannot?
2. What is the difference between total time (`tottime`) and cumulative time (`cumtime`) in profiling output?
3. How does continuous sampling profiling (e.g. py-spy) differ from deterministic instrumentation profiling?

## What comes next
Having understood application profiling, we next discover its inherent boundaries and transition to **Memory Leaks**.
