# Lesson 33: Search Basics

> **Motto**: Relational databases provide capable search mechanisms; introducing Elasticsearch prematurely introduces massive operational complexity.

---

## Motto
"Relational databases provide capable search mechanisms; introducing Elasticsearch prematurely introduces massive operational complexity."

## Problem
Teams immediately deploy separate search clusters for simple substring searches, introducing data drift and sync bugs.

## Prediction
Utilizing SQL `LIKE`, trigram indexes (`pg_trgm`), or PostgreSQL full-text search (`tsvector`) handles most early requirements.

## Why this matters
Understanding the limits of SQL search defines exactly when an external search engine becomes truly justified.

## First principles
Full-text search: Text -> Tokenization -> Stemming -> Inverted Index -> Ranked Query Results.

## Mental model
```text
Search Query -> Lowercase & Tokenize -> Inverted Index / GIN Index Match -> Ranked Relevance Results
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Search endpoint with tokenized multi-word search and relevance ordering.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/33-search-basics/tests/ -v
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
- **Failure Injection**: Search for words with varying suffixes ('run', 'running', 'runner') and verify stemming matches.
- Execute the experiment script:
```bash
python phases/33-search-basics/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that full-text inverted index resolves queries without full table scans.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Add GIN indexes to full-text columns to ensure logarithmic search performance.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Search endpoints can be exploited for ReDoS or intensive CPU exhaustion; enforce minimum query length (e.g. 3 chars).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Only migrate to Elasticsearch or OpenSearch when you require complex typo tolerance, faceted search, or petabyte scale.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is an inverted index and how does it speed up text search?
2. What is the difference between SQL 'LIKE %term%' and full-text search with stemming?
3. At what scale or requirement does migrating from PostgreSQL full-text search to Elasticsearch become justified?

## What comes next
Having understood search basics, we next discover its inherent boundaries and transition to **Authentication Problem**.
