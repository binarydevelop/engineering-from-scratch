# Lesson 22.1: N-grams

## Motto
"N-grams trade disk storage for lookup velocity: generate substrings at index time to avoid wildcards at query time."

## Problem
Searching inside words (substring matching, e.g. finding `"1234"` inside serial number `"AB-1234-XYZ"`) requires expensive regex scans unless substrings are pre-indexed.

## Prediction
If you generate 3-grams to 5-grams for every word in a document, by what multiple will the number of indexed terms increase?

## Why this matters
N-grams are essential for non-spaced languages (Chinese, Japanese), partial SKU matching, and fuzzy autocomplete. But careless n-gram configurations can explode index disk size by $5	imes$ to $20	imes$.

## First principles
An **n-gram** is a contiguous sequence of $n$ characters:
* Word: `"elastic"`
* 3-grams: `["ela", "las", "ast", "sti", "tic"]`
* **Edge n-grams:** Only sequences anchored to the start of the word:
  `["el", "ela", "elas", "elast", "elasti", "elastic"]`

## Mental model
```text
Standard Token:  "search" ──► 1 term in index
3-to-4 N-grams:  "search" ──► ["sea", "sear", "ear", "earc", "arc", "arch", "rch"] (7 terms!)
                              Disk space expands significantly!
```

## Build it
See `code/ngram_generator.py` measuring term multiplication factor across sample texts.

## Use Elasticsearch
Run the experiment:
```bash
./phases/22-n-grams/experiments/run_experiment.sh
```

## Inspect it
Use `_analyze` with an `ngram` token filter:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": [
    { "type": "ngram", "min_gram": 3, "max_gram": 4 }
  ],
  "text": "elastic"
}'
```

## Measure it
Measure index disk size before and after adding n-gram analysis.

## Break it
Configure `min_gram: 1` and `max_gram: 10` on large text bodies and observe disk storage and indexing latency skyrocket.

## Recover it
Constrain n-grams: use `edge_ngram` anchored to word boundaries with `min_gram: 2` and `max_gram: 8`.

## Modify it
Compare `ngram` vs `edge_ngram` for search-as-you-type.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an edge n-gram produce fewer terms than a standard n-gram?
2. When should n-gram filters be applied at index time versus search time?

## Guarantees
* Pre-indexing n-grams converts substring searches into instant exact term lookups.

## Non-guarantees
* N-grams do not prevent disk bloat if grammar bounds are set too wide.

## When to use this
* Partial serial numbers, code fragments, and language-independent substring search.

## When not to use this
* Large body paragraphs or general natural language articles.

## What comes next
In Phase 23, we synthesize these tools into a complete Search-As-You-Type design.
