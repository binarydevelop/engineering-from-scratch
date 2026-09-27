# Lesson 43.1: Document Routing

## Motto
"Shard = hash(routing_value) % num_primary_shards: custom routing eliminates scatter-gather by isolating searches to one shard."

## Problem
In a multi-tenant SaaS application with 10,000 corporate customers, every customer search queries ALL shards across the entire cluster (scatter-gather). Even though Customer 42's data is only 10MB, the query wastes resources hitting 20 different nodes!

## Prediction
Can you force all documents belonging to a specific customer to live on the exact same shard, so customer queries only hit a single shard?

## Why this matters
The default routing formula is:
$$	ext{shard} = 	ext{hash}(	ext{_id}) \pmod{	ext{number\_of\_primary\_shards}}$$
By supplying a custom routing key (`_routing`), you can co-locate related documents on one shard, eliminating distributed network fan-out!

## First principles
* **Default Routing:** Uniform hash distribution across all shards. Great for balanced disk usage, but requires scatter-gather across all shards for searches.
* **Custom Routing (`?routing=tenant_123`):** Hashes the routing value instead of `_id`. All documents for that tenant land on the exact same shard.
* Searches with `?routing=tenant_123` hit **exactly one shard**!

## Mental model
```text
Default Search:
  GET /orders/_search?q=laptop
  Coordinating Node ──► Scatter to Shard 0, Shard 1, Shard 2 (All Shards!)

Custom Routing Search:
  GET /orders/_search?routing=tenant_42&q=laptop
  Coordinating Node ──► Hits ONLY Shard 1! (Zero Fan-Out!)
```

## Build it
See `code/custom_routing_sim.py` demonstrating single-shard targeted queries vs multi-shard broadcast.

## Use Elasticsearch
Run the experiment:
```bash
./phases/43-document-routing/experiments/run_experiment.sh
```

## Inspect it
Index documents with custom routing and verify shard placement:
```bash
curl -X PUT "http://localhost:9200/routing_demo/_doc/1?routing=company_a" -H "Content-Type: application/json" -d '{"company": "company_a", "val": 100}'
curl -X PUT "http://localhost:9200/routing_demo/_doc/2?routing=company_a" -H "Content-Type: application/json" -d '{"company": "company_a", "val": 200}'
```
Query with `_search?routing=company_a` and check `_shards.total: 1` in the response header!

## Measure it
Compare query QPS: targeted single-shard searches can achieve 5x to 10x higher cluster throughput than scatter-gather queries.

## Break it
Route 90% of all data to a single tenant key (`routing=uber_tenant`). That single shard becomes a massive **Hot Shard**, while other shards sit idle!

## Recover it
Use `index.routing_partition_size` to spread a custom routing key across a bounded subset of shards.

## Modify it
Enforce mandatory routing in the mapping: `"_routing": { "required": true }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does changing the number of primary shards break document routing?
2. What is the risk of using custom routing with an uneven data distribution?

## Guarantees
* Custom routing guarantees all documents sharing a routing key are stored on the same shard.

## Non-guarantees
* Custom routing does not guarantee balanced disk space across nodes if tenant sizes vary wildly.

## When to use this
* Multi-tenant SaaS architectures, user-partitioned social feeds, and time-series session stores.

## When not to use this
* Public global catalogs where queries span all items globally.

## What comes next
In Phase 44, we trace Distributed Search: scatter-gather query coordination across nodes.
