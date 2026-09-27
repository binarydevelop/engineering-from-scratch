# Lesson 14.1: TF-IDF Intuition

## Motto
"Common words carry little information; rare words carry immense signal."

## Problem
When searching for `"the elasticsearch architecture"`, every English document contains `"the"`. If `"the"` is scored equally with `"elasticsearch"`, documents will be ranked based on how often they use stop words rather than whether they discuss Elasticsearch.

## Prediction
If a query contains two terms, one appearing in 90% of documents and one appearing in 0.1% of documents, how much more weight should the rare term receive?

## Why this matters
TF-IDF (Term Frequency-Inverse Document Frequency) established modern Information Retrieval. It mathematically formalizes the intuition of term informativeness.

## First principles
* **Term Frequency (TF):** Measures local importance within a document: $	ext{TF}(t, d)$.
* **Inverse Document Frequency (IDF):** Measures global rarity across corpus:
  $$	ext{IDF}(t) = \ln\left(1 + rac{N}{	ext{DF}(t)}ight)$$
  Where $N$ is total documents, and $	ext{DF}(t)$ is number of documents containing term $t$.
* **Score:** $	ext{TF}(t, d) 	imes 	ext{IDF}(t)$.

## Mental model
```text
Term: "the"           ──► In 10,000 of 10,000 docs ──► IDF ≈ ln(1 + 1) ≈ 0.69 (Low Signal)
Term: "elasticsearch" ──► In 5 of 10,000 docs      ──► IDF ≈ ln(1 + 2000) ≈ 7.60 (High Signal!)
```

## Build it
See `code/tfidf_scorer.py` computing TF-IDF across a multi-document corpus in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/14-tf-idf-intuition/experiments/run_experiment.sh
```

## Inspect it
Observe how matching a rare term dramatically outscores matching common terms.

## Measure it
Compare scores for multi-term queries where one term is rare and one is frequent.

## Break it
Notice what happens as term frequency in a document increases from 10 to 1,000: in classic TF-IDF, score increases linearly without bound, enabling keyword stuffing.

## Recover it
Introduce term frequency saturation (BM25 in Phase 15).

## Modify it
Vary corpus size $N$ from 100 to 1,000,000 and plot the IDF curve.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does IDF use a logarithmic scale rather than a linear scale?
2. What happens to the IDF of a term that appears in every single document in the index?

## Guarantees
* Rare terms receive exponentially higher relative weighting than common terms.

## Non-guarantees
* Classic TF-IDF does not prevent score distortion from repeated terms in long documents.

## When to use this
* As the foundational conceptual framework before understanding BM25.

## When not to use this
* Elasticsearch 8.x uses BM25 by default; do not implement raw TF-IDF manually in production.

## What comes next
In Phase 15, we implement BM25 (Best Matching 25), the default relevance engine of Elasticsearch.
