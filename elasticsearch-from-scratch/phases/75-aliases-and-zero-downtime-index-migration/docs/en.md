# Lesson 75.1: Aliases and Zero-Downtime Index Migration

## Motto
"Never query physical index names: point clients to an alias, reindex to v2, and swap aliases atomically in 0.001 ms."

## Problem
You need to reindex from `products_v1` to `products_v2`. If client applications hardcode the URL `http://es:9200/products_v1/_search`, how do you switch traffic to `products_v2` without updating code, redeploying 50 microservices, or incurring downtime?

## Prediction
Can you atomically swap traffic from `products_v1` to `products_v2` in a single master metadata transaction with zero dropped queries?

## Why this matters
**Index Aliases** decouple logical application index names from physical versioned indices. Aliases enable zero-downtime schema migrations.

## First principles
The Atomic Alias Swap:
* Clients always query `http://es:9200/products/_search` (where `products` is an alias).
* While live traffic hits `products_v1`, you build `products_v2` and reindex in the background.
* Execute an atomic alias update:
  * Remove `products` from `products_v1`
  * Add `products` to `products_v2`
* Elasticsearch executes this swap inside the cluster state in **sub-millisecond time**. Zero dropped requests!

## Mental model
```text
Step 1: Steady State
  Client ──► Alias "products" ──► Physical Index [products_v1]

Step 2: Reindexing in Background
  Client ──► Alias "products" ──► Physical Index [products_v1]
                                 [products_v2] (Hydrating via _reindex...)

Step 3: Atomic Swap (0.001 ms)
  Client ──► Alias "products" ──► Physical Index [products_v2]!
  (Old products_v1 can now be safely deleted!)
```

## Build it
See `code/atomic_alias_sim.py` demonstrating pointer swaps in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/75-aliases-and-zero-downtime-index-migration/experiments/run_experiment.sh
```

## Inspect it
Check alias mappings:
```bash
curl -s "http://localhost:9200/_cat/aliases?v"
```

## Measure it
Measure latency of the alias swap API call (< 5ms).

## Break it
Delete an index that has an alias pointing to it without re-pointing the alias. Queries hitting the alias fail immediately.

## Recover it
Always add the new index before or atomically during the removal of the old index.

## Modify it
Create a filtered alias: an alias that automatically restricts queries to a specific tenant:
`"filter": { "term": { "tenant_id": "corp_42" } }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must the alias removal and addition occur within the same `_aliases` API request?
2. What is a "filtered alias" and how does it simplify application security?

## Guarantees
* Alias swaps are atomic: a query will either execute against v1 or v2; never against a non-existent state.

## Non-guarantees
* An alias cannot prevent write conflicts if clients continue writing to v1 during reindexing.

## When to use this
* Every production index (never query physical index names directly).

## When not to use this
* Temporary scratch testing scripts.

## What comes next
In Phase 76, we configure Elasticsearch Security Basics: TLS, RBAC, and users.
