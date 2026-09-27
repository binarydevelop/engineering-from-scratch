# Lesson 15.1: BM25 (Best Matching 25)

## Motto
"BM25 solves the two flaws of TF-IDF: it saturates term frequency and normalizes by field length."

## Problem
In classic TF-IDF, if a spammer repeats `"cheap flights"` 500 times in a page, their score is 500 times higher than a genuine document with 1 mention. Furthermore, a 10,000-word book naturally contains more mentions than a 50-word product description.

## Prediction
In BM25, does repeating a term 100 times give you 100x the score of mentioning it once, or does the score asymptotically approach an upper ceiling?

## Why this matters
BM25 is the default scoring algorithm in Elasticsearch 8.17.0 and Apache Lucene. Every relevance score you see in `_search` is computed by BM25.

## First principles
BM25 formula for term $q$:
$$	ext{Score}(D, q) = 	ext{IDF}(q) 	imes rac{	ext{TF} 	imes (k_1 + 1)}{	ext{TF} + k_1 	imes \left(1 - b + b 	imes rac{|D|}{	ext{avgdl}}ight)}$$
Parameters in Elasticsearch 8.17.0:
* $k_1 = 1.2$: Controls **TF saturation**. As TF grows, the multiplier saturates at $(k_1 + 1) = 2.2$.
* $b = 0.75$: Controls **field length normalization**.
  * If $b = 1.0$, length penalty is fully applied.
  * If $b = 0.0$, document length is ignored completely.

## Mental model
```text
Score Multiplier
   ▲
2.2│                       ┌──────────────────────── Asymptotic Ceiling (k1 + 1)
   │                  . ' '
1.5│             . '
   │         . '
1.0│     . '
   │  . '
   └────────────────────────────────────────► Term Frequency (TF)
      1   2   3   4   5   10  20  50  100
```

## Build it
See `code/bm25_scorer.py` implementing the complete BM25 formula from scratch.

## Use Elasticsearch
Run the experiment:
```bash
./phases/15-bm25/experiments/run_experiment.sh
```

## Inspect it
Compare Python BM25 scores with Elasticsearch `_explain` outputs.

## Measure it
Plot the term frequency saturation curve for $	ext{TF} \in [1, 50]$.

## Break it
Set $b = 0.0$ in custom similarity and observe how long, keyword-stuffed documents outrank short, concise titles.

## Recover it
Restore default $b = 0.75$.

## Modify it
Adjust $k_1$ from 1.2 to 2.0 to give more weight to repeated terms in technical documentation.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does BM25 saturate term frequency while classic TF-IDF does not?
2. What is the effect of setting parameter $b = 0$ on field length normalization?

## Guarantees
* An author cannot arbitrarily inflate relevance score by repeating a term infinitely.

## Non-guarantees
* BM25 does not understand semantic context or synonyms out of the box.

## When to use this
* Default relevance scoring for full-text search across documents and articles.

## When not to use this
* Exact matching, categorical filtering, or vector similarity.

## What comes next
In Phase 16, we dissect how to inspect and explain relevance scores using Elasticsearch's `_explain` API.
