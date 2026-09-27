# Lesson 69.1: Search API Design

## Motto
"Never leak raw query DSL to the public internet: encapsulate search behind a strongly typed, validated API gateway."

## Problem
A naive backend exposes a pass-through endpoint `POST /api/search` that forwards the user's JSON directly into Elasticsearch `_search`. An attacker injects leading wildcards, deep paginations (`from: 1000000`), or fielddata aggregations on sensitive internal fields, bringing down the entire cluster.

## Prediction
Why is exposing raw Elasticsearch JSON DSL to public frontend clients considered a critical security and performance vulnerability?

## Why this matters
Search API gateways enforce query sanitation, parameter validation, default filters (e.g. `tenant_id`, `deleted: false`), max page windows, and rate limits.

## First principles
API Gateway Responsibilities:
1. **Contract Abstraction:** Accepts clean query params: `GET /search?q=wireless&category=tech&page=2`.
2. **Mandatory Tenant Isolation:** Injects security filter context (`tenant_id: auth_user.tenant_id`) that the user cannot override.
3. **Pagination Bounding:** Caps `size <= 50` and prevents deep pagination.
4. **DSL Construction:** Translates safe parameters into an optimized compound `bool` query.

## Mental model
```text
Public Client (Browser / Mobile)
          │ GET /v1/products?q=chair&min_price=100
          ▼
   API GATEWAY (Python / FastAPI / Express)
          ├── 1. Validate & Sanitize Input
          ├── 2. Inject Security Filters (tenant_id = 42)
          ├── 3. Enforce Max Result Window (page <= 20)
          └── 4. Construct Safe Elasticsearch Bool Query
                         │
                         ▼
        ELASTICSEARCH CLUSTER (Internal Network)
```

## Build it
See `code/search_gateway.py` implementing a clean parameter-to-DSL translation layer in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/69-search-api-design/experiments/run_experiment.sh
```

## Inspect it
Test the gateway's query generator with various input parameters.

## Measure it
Measure latency added by the translation layer (typically < 0.2ms in Python).

## Break it
Send an injection attempt (`q="*.*.*"`, `from=9999999`) and observe how the gateway rejects or sanitizes the input before reaching Elasticsearch.

## Recover it
Always validate query parameters using strict schemas (e.g. Pydantic).

## Modify it
Add highlighting configurations to return text snippets with `<em>` tags.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What attacks are possible when raw Elasticsearch query DSL is exposed directly to clients?
2. How does the search gateway guarantee multi-tenant data isolation?

## Guarantees
* The gateway guarantees that no unvalidated query shapes reach the cluster.

## Non-guarantees
* The gateway does not replace cluster-side resource limits.

## When to use this
* Every production search service.

## When not to use this
* Internal cluster debugging using `curl`.

## What comes next
In Phase 70, we build Capstone 1: The Complete Product Search Project.
