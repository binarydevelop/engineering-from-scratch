# Lesson 73.1: Synonym and Relevance Tuning

## Motto
"Relevance tuning is multi-variable optimization: balance field boosts, synonyms, and phrase slop against evaluation metrics."

## Problem
In catalog search, users search for `"apple laptop"`. If the product brand is `"Apple"` and category is `"laptop"`, but title is `"MacBook Pro"`, a standard match query fails to rank the document at the top.

## Prediction
How can you combine multi-match field boosting, synonyms, and cross-fields matching to maximize MRR?

## Why this matters
Relevance tuning balances recall (finding all reasonable matches) with precision (placing the best match at rank 1).

## First principles
Tuning Levers:
1. **Field Boosts:** `title^3`, `brand^2`, `category^1.5`. Gives higher weight to matches in concise fields.
2. **`cross_fields` Type:** Treats all fields as a single combined document, so `"apple"` in brand and `"laptop"` in category satisfy the query together!
3. **Phrase Slop Boosting:** Uses `should` with `match_phrase` (slop 1) to give bonus points to documents where words appear adjacent.

## Mental model
```text
Query: "apple laptop"
  ├── Must match: cross_fields on [brand, category, title] (Recall)
  └── Should match: match_phrase on title with boost^2 (Precision bonus for adjacency!)
```

## Build it
See `code/relevance_tuning_experiment.py` running benchmark comparisons in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/73-synonym-and-relevance-tuning/experiments/run_experiment.sh
```

## Inspect it
Test `multi_match` with `cross_fields`:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "multi_match": {
      "query": "wireless keyboard",
      "type": "cross_fields",
      "fields": ["title^3", "category^1.5"]
    }
  }
}'
```

## Measure it
Compare Precision@5 before and after adding phrase boost.

## Break it
Assign an extreme boost (`title^1000`): observe that relevance scores for title matches completely drown out category and brand filters.

## Recover it
Keep boosts moderate (typically $1.2	imes$ to $3.0	imes$).

## Modify it
Add `tie_breaker: 0.3` to include signals from secondary matching fields.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `multi_match` with `type: cross_fields` solve term distribution across multiple columns?
2. What is the danger of setting arbitrary boost factors (> 50)?

## Guarantees
* Boost factors deterministically scale BM25 term weights.

## Non-guarantees
* Boosting cannot fix missing terms if the tokenizer discarded them.

## When to use this
* Fine-tuning catalog search, knowledge bases, and document archives.

## When not to use this
* Exact status queries or log filtering.

## What comes next
In Phase 74, we master Reindexing when mapping changes are required.
