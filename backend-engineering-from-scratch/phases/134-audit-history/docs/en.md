# Lesson 134: Audit History

> **Motto**: Audit history tracks the complete historical evolution of database records over time, capturing who changed what and when.

---

## Motto
"Audit history tracks the complete historical evolution of database records over time, capturing who changed what and when."

## Problem
Overwriting row values with `UPDATE` erases previous state, making it impossible to know what a record looked like last week.

## Prediction
Using historical change tables, temporal tables, or event streams records every modification for auditing and dispute resolution.

## Why this matters
Audit history provides complete traceability for financial accounts, legal contracts, and medical records.

## First principles
Current State Table (`orders`) + History Table (`order_history` with `version, changed_by, old_values, new_values, timestamp`).

## Mental model
```text
UPDATE order SET status = 'shipped' -> Trigger / App writes row into order_history -> Full historical timeline preserved
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: PostgreSQL triggers / SQLAlchemy event listeners for automated history tracking.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/134-audit-history/tests/ -v
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
- **Failure Injection**: Update an order record three times (Created -> Paid -> Shipped); query the audit history table.
- Execute the experiment script:
```bash
python phases/134-audit-history/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify history table records all three revisions with accurate diffs, actor IDs, and timestamps.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Store field changes as JSON diffs (`{"status": ["paid", "shipped"]}`) to keep history storage efficient.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: History tables grow rapidly; implement retention policies and table partitioning by timestamp.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Do not confuse simple audit history with full Event Sourcing; audit history is significantly simpler to build and operate.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does overwriting rows with UPDATE statements destroy institutional forensic evidence?
2. What are the tradeoffs of storing full row snapshots versus JSON field diffs in history tables?
3. How does database table partitioning help manage the growth of historical audit tables?

## What comes next
Having understood audit history, we next discover its inherent boundaries and transition to **Webhooks**.
