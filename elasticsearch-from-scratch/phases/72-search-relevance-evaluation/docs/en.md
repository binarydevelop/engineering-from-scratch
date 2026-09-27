# Lesson 72.1: Search Relevance Evaluation

## Motto
"Search quality is not a feeling: quantify relevance with Precision@K, Mean Reciprocal Rank, and NDCG."

## Problem
A developer changes a query boost: `title^2` to `title^4`. They test one query on their laptop, decide "it looks better", and deploy to production. In doing so, they silently degrade search results for 40% of customer queries!

## Prediction
How can you objectively measure whether a change to Elasticsearch rankings improved or harmed search results across a test suite of 100 queries?

## Why this matters
Relevance engineering is an empirical science. Professional search teams use quantitative evaluation metrics.

## First principles
Core Information Retrieval Metrics:
1. **Precision@K:** What fraction of the top $K$ results are relevant?
   $$	ext{Precision@K} = rac{|	ext{Relevant Docs in Top } K|}{K}$$
2. **Mean Reciprocal Rank (MRR):** How quickly does the user find the first relevant document? (Reciprocal of the rank position of the first relevant result).
3. **NDCG (Normalized Discounted Cumulative Gain):** Rewards placing highly relevant documents near the very top of the list.

## Mental model
```text
Query: "wireless keyboard"
  Ground Truth Relevant Docs: [Doc A, Doc B]

Result 1: [Doc A, Doc B, Doc C] ──► Precision@3 = 2/3 = 66%, MRR = 1.0 (First doc relevant!)
Result 2: [Doc X, Doc Y, Doc A] ──► Precision@3 = 1/3 = 33%, MRR = 0.33 (Relevant doc buried at rank 3)
```

## Build it
See `code/relevance_evaluator.py` computing Precision@K and MRR in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/72-search-relevance-evaluation/experiments/run_experiment.sh
```

## Inspect it
Use Elasticsearch's native **Ranking Evaluation API** (`_rank_eval`):
```bash
curl -X POST http://localhost:9200/products_phase06/_rank_eval -H "Content-Type: application/json" -d '{
  "requests": [
    {
      "id": "keyboard_query",
      "request": { "query": { "match": { "title": "keyboard" } } },
      "ratings": [
        { "_index": "products_phase06", "_id": "1", "rating": 3 }
      ]
    }
  ],
  "metric": { "precision": { "k": 5 } }
}'
```

## Measure it
Compare MRR scores before and after applying field boosts.

## Break it
Tune rankings for one query while measuring the whole suite: observe how over-fitting to one query hurts overall MRR.

## Recover it
Maintain a diverse golden evaluation dataset spanning common head queries and rare tail queries.

## Modify it
Test NDCG metric with graded ratings (0=irrelevant, 1=marginal, 2=relevant, 3=perfect).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is measuring search quality on a single query misleading?
2. What does a Mean Reciprocal Rank (MRR) of 0.5 indicate? (The first relevant hit appears on average at rank 2).

## Guarantees
* Ranking evaluation provides statistical confidence for relevance changes.

## Non-guarantees
* Metrics are only as good as the ground-truth relevance judgment dataset.

## When to use this
* Every search relevance change, boost tuning, and analyzer modification.

## When not to use this
* Pure operational logging clusters where BM25 relevance is not used.

## What comes next
In Phase 73, we apply these evaluation metrics to Synonym and Relevance Tuning.
