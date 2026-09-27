# Lesson 11.1: Boolean Search

## Motto
"Boolean queries are set algebra with relevance: must intersects, should boosts, filter excludes scoring, must_not inverts."

## Problem
Users rarely search for single words. They want: "wireless keyboard, under $100, preferably mechanical, but NOT refurbished". Representing this in search requires combining multiple independent clauses with distinct scoring rules.

## Prediction
In a `bool` query, does a clause in the `should` section require a document to match if `must` clauses are already present?

## Why this matters
The `bool` query is the workhorse of Elasticsearch query composition. Almost every production search query is wrapped in a `bool` container.

## First principles
The four clauses of `bool`:
* `must`: Logical AND. Document MUST match. Score is added to total score.
* `filter`: Logical AND. Document MUST match. Score is ignored ($0.0$). Results are cached.
* `should`: Logical OR / Boost. If `must` is present, `should` acts as an optional score booster. If no `must` is present, at least one `should` clause must match (`minimum_should_match: 1`).
* `must_not`: Logical NOT. Document MUST NOT match. Executed in filter context.

## Mental model
```text
                    BOOL QUERY
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
   MUST              FILTER            SHOULD
 (Intersection)    (Binary Check)   (Score Booster)
 (Affects Score)   (Score = 0.0)    (Optional if Must)
```

## Build it
See `code/bool_search.py` implementing `must`, `should`, and `must_not` over postings lists.

## Use Elasticsearch
Run the experiment:
```bash
./phases/11-boolean-search/experiments/run_experiment.sh
```

## Inspect it
Test `bool` with must, filter, and should:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "must": [{ "match": { "title": "keyboard" } }],
      "filter": [{ "range": { "price": { "lte": 150 } } }],
      "should": [{ "match": { "title": "mechanical" } }],
      "must_not": [{ "term": { "category": "furniture" } }]
    }
  }
}'
```

## Measure it
Compare scoring breakdown: documents matching the `should` clause receive higher scores than documents matching only `must`.

## Break it
Set `minimum_should_match: 2` when only 1 should clause exists and observe zero hits.

## Recover it
Align `minimum_should_match` with available should clauses.

## Modify it
Add `boost: 2.0` to the `should` clause and observe ranking reordering.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `filter` improve query speed compared to `must`?
2. When does a `should` clause become mandatory?

## Guarantees
* `bool` enforces exact boolean set logic across all clauses.

## Non-guarantees
* `bool` does not prevent slow execution if interior clauses contain unindexed wildcards.

## When to use this
* Standard application search forms with multiple filters and keywords.

## When not to use this
* Simple single-term exact lookups (use a single `term` query directly).

## What comes next
In Phase 12, we measure the performance and scoring differences between Query Context and Filter Context.
