# Lesson 23.1: Search-As-You-Type Design

## Motto
"A great search-as-you-type experience balances prefix matching, ranking popularity, and typo resilience."

## Problem
Building a responsive search bar requires handling unfinished words (`wirel`), partial terms (`keyb`), and occasional typos simultaneously, while ranking popular items higher than obscure matches.

## Prediction
What mapping configuration allows matching prefixes on the last entered token while applying BM25 scoring and popularity boosts?

## Why this matters
Elasticsearch provides the dedicated `search_as_you_type` field type (introduced in 7.x and mature in 8.x) that automatically creates root, 2-gram, and 3-gram shingle subfields.

## First principles
The `search_as_you_type` field type generates:
* `field`: standard analyzed text
* `field._2gram`: 2-word shingles with edge n-grams
* `field._3gram`: 3-word shingles with edge n-grams
* `field._index_prefix`: edge n-grams on the last term

## Mental model
```text
User Types: "wireless mech"
                  │
   [ Multi-Match bool query ]
      ├── Match on root text
      └── Prefix match on _index_prefix / _2gram
                  │
                  ▼
Result: "Wireless Mechanical Gaming Keyboard" (Instant Hit)
```

## Build it
See `code/search_as_you_type_sim.py` demonstrating query rewriting for prefix and popularity weighting.

## Use Elasticsearch
Run the experiment:
```bash
./phases/23-search-as-you-type-design/experiments/run_experiment.sh
```

## Inspect it
Create an index with `search_as_you_type` and inspect its generated subfields:
```bash
curl -X PUT http://localhost:9200/sayt_demo -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "name": { "type": "search_as_you_type" }
    }
  }
}'
```

## Measure it
Measure query latency as query length increases from 1 to 10 characters.

## Break it
Use `search_as_you_type` on large article body fields instead of short title/name fields.

## Recover it
Restrict `search_as_you_type` to short titles, product names, and navigation entities.

## Modify it
Add function score or field value factor (`boost: popularity`) to sort suggestions by customer purchase volume.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `search_as_you_type` automatically create 2-gram and 3-gram subfields?
2. How does `bool` query structure ensure complete words are scored higher than partial prefixes?

## Guarantees
* Provides sub-15ms prefix search without managing custom analyzer chains manually.

## Non-guarantees
* Consumes more disk space than standard `text` fields due to automatic shingle subfields.

## When to use this
* E-commerce, SaaS, and document catalog search bars.

## When not to use this
* Massive unstructured text bodies.

## What comes next
In Phase 24, we shift from textual analysis to Numeric and Date Fields (BKD Trees).
