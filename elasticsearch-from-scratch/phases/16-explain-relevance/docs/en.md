# Lesson 16.1: Explain Relevance

## Motto
"Relevance is not magic; every floating point score is an audited sum of IDF, TF saturation, and length normalization."

## Problem
In production, a stakeholder asks: *"Why did Document 42 rank higher than Document 88 for query 'gaming laptop'?"* Guessing leads to arbitrary boost tweaks that degrade overall search quality.

## Prediction
Can you determine from an API call the exact numeric contribution of term frequency versus inverse document frequency for a specific document?

## Why this matters
The `_explain` API provides complete transparency into Lucene's scoring calculation. It turns relevance debugging from guesswork into mathematical verification.

## First principles
The `_explain` response decomposes the score into a hierarchical tree:
* Top-level: sum of matching query clauses
* Each clause: `weight(title:keyword in doc_id)`
  * `idf`: calculated from doc count
  * `tf`: calculated with $k_1$ and $b$ length normalization factor

## Mental model
```text
Score: 2.451
  ├── weight(title:gaming in 42): 1.120
  │     ├── idf: 1.450
  │     └── tfNorm: 0.772 (tf=1, len=4, avgdl=6.2)
  └── weight(title:laptop in 42): 1.331
        ├── idf: 1.820
        └── tfNorm: 0.731 (tf=1, len=4, avgdl=6.2)
```

## Build it
See `code/parse_explain.py` illustrating how to parse and summarize Lucene explain trees in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/16-explain-relevance/experiments/run_experiment.sh
```

## Inspect it
Request an explain plan for a specific document ID:
```bash
curl -X POST http://localhost:9200/products_phase06/_explain/1 -H "Content-Type: application/json" -d '{
  "query": { "match": { "title": "chair" } }
}'
```

## Measure it
Notice the overhead: running `_explain` computes verbose descriptions and should never be enabled for high-QPS user queries.

## Break it
Run `explain: true` across 1,000 search results and observe response payload size jump to several megabytes.

## Recover it
Use `_explain` only on targeted single-document requests during relevance debugging.

## Modify it
Add a field boost (`title:chair^2.0`) and observe how the explain tree introduces a `boost: 2.0` multiplier node.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the explain tree show both `freq` (raw term count) and `tfNorm`?
2. Why is running `_explain` in production search endpoints dangerous?

## Guarantees
* The explain tree accounts for 100% of the mathematical score returned by `_search`.

## Non-guarantees
* `_explain` does not diagnose queries that fail to match candidate documents (zero hits).

## When to use this
* Investigating ranking anomalies and tuning weights/boosts.

## When not to use this
* Public customer-facing search APIs.

## What comes next
In Phase 17, we explore Phrase Search: matching words that appear in specific sequence.
