# Lesson 17.1: Phrase Search

## Motto
"Words in proximity carry meaning that isolated terms lose: position matters."

## Problem
Searching for `"distributed systems"` should match a book on distributed computing, but should NOT rank a document that says: *"The system was distributed across three offices and had multiple plumbing systems."* Term matching alone cannot differentiate adjacent words from words separated by 50 paragraphs.

## Prediction
Will a document containing `"distributed operating systems"` match a `match_phrase` query for `"distributed systems"` with default parameters? What about with `slop: 1`?

## Why this matters
Phrase search preserves semantic word groupings. It relies on term positions recorded in Lucene's `.pos` inverted index files.

## First principles
* **Positional Postings List:** Stores not just Doc ID, but the exact token position indices:
  `"distributed" -> [Doc 1 (pos: 0)]`
  `"systems" -> [Doc 1 (pos: 1)]`
* **Match:** Adjacent positions `pos("systems") - pos("distributed") == 1`.
* **Slop:** The number of position moves or edits allowed between terms. `slop: 1` allows 1 intervening word.

## Mental model
```text
Doc 1: "Distributed [0] Systems [1]" ──► Adjacent (diff = 1) ──► Match Phrase (slop=0)
Doc 2: "Distributed [0] Database [1] Systems [2]" ──► Intervening word ──► Match Phrase (slop=1)
```

## Build it
See `code/positional_index.py` building a positional index and phrase matcher in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/17-phrase-search/experiments/run_experiment.sh
```

## Inspect it
Test `match_phrase` with varying slop values:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "match_phrase": {
      "title": { "query": "ergonomic chair", "slop": 0 }
    }
  }
}'
```

## Measure it
Compare phrase query execution time against a standard boolean `match` query: phrase search is slower because it must intersect token positions, not just document IDs.

## Break it
Increase slop to 100 on a long document corpus and observe query latency rise due to wide positional window checks.

## Recover it
Keep slop low (0 to 2) for strict phrase matching.

## Modify it
Use `match_phrase_prefix` for autocomplete search.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does storing term positions increase the size of an inverted index on disk?
2. What does a `slop` of 2 permit between two query terms?

## Guarantees
* `match_phrase` guarantees that terms appear in the specified relative order within the slop window.

## Non-guarantees
* Phrase queries do not evaluate semantic similarity beyond token order.

## When to use this
* Exact titles, quotes, technical idioms, and address matching.

## When not to use this
* Broad exploratory queries where word order is irrelevant.

## What comes next
In Phase 18, we investigate Prefix, Wildcard, and Regex queries.
