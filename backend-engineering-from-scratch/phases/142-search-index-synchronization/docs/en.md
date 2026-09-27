# Lesson 142: Search Index Synchronization

> **Motto**: Search index synchronization updates external search clusters asynchronously when primary database records change.

---

## Motto
"Search index synchronization updates external search clusters asynchronously when primary database records change."

## Problem
Updating Elasticsearch synchronously inside an SQL write transaction introduces distributed transaction failures and latency.

## Prediction
Using asynchronous event streams or Transactional Outbox workers to update search indexes guarantees eventual consistency.

## Why this matters
Decoupled search indexing ensures that search cluster downtime never blocks primary database writes.

## First principles
PostgreSQL Write -> Commit Transaction -> Outbox Event -> Indexer Worker reads Event -> Updates Elasticsearch Document.

## Mental model
```text
SQL Mutation ──[Committed]──> Outbox Table ──> Indexing Worker ──> Updates Elasticsearch Document
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Change Data Capture (Debezium) and event-driven search indexing pipelines.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/142-search-index-synchronization/tests/ -v
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
- **Failure Injection**: Update a product in the primary database; observe outbox event emitted; verify indexer updates search document.
- Execute the experiment script:
```bash
python phases/142-search-index-synchronization/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Simulate search cluster downtime during database write; observe outbox preserves event and retries until indexer succeeds.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement full re-indexing scripts: provide the ability to rebuild the entire search index from scratch from PostgreSQL.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Handle out-of-order updates: use database version numbers (`version`) to prevent older events from overwriting newer index data.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Accept eventual consistency: inform users that search results may take 500ms to reflect immediate database updates.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is updating Elasticsearch synchronously inside a database transaction an operational anti-pattern?
2. How does the Transactional Outbox pattern guarantee search index consistency when the search cluster experiences downtime?
3. How do version numbers prevent out-of-order event updates from corrupting a search index?

## What comes next
Having understood search index synchronization, we next discover its inherent boundaries and transition to **Cache as Derived Data**.
