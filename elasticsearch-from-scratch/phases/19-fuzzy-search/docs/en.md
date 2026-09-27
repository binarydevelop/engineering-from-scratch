# Lesson 19.1: Fuzzy Search

## Motto
"Fuzziness is typo tolerance via Damerau-Levenshtein edit distance, NOT semantic similarity."

## Problem
Users misspell words frequently: `"elastcisearch"`, `"phne"`, `"macbok"`. If a search engine only performs exact term lookup, any typo results in zero hits and lost conversions.

## Prediction
Will a fuzzy query with `fuzziness: 1` match `"phone"` when the user types `"phne"`? What if the user types `"fone"`?

## Why this matters
Fuzzy matching recovers from human typing mistakes. However, beginners confuse character edit distance with conceptual similarity.

## First principles
Fuzzy matching calculates the **Damerau-Levenshtein Distance**: the minimum number of single-character operations required to transform word $A$ into word $B$:
1. Insertion (`cst` -> `cost`)
2. Deletion (`coost` -> `cost`)
3. Substitution (`cast` -> `cost`)
4. Transposition of adjacent characters (`csot` -> `cost`)
In Elasticsearch, `fuzziness: "AUTO"` chooses distance based on word length:
* 0..2 chars: edit distance 0 (exact match)
* 3..5 chars: edit distance 1
* > 5 chars: edit distance 2

## Mental model
```text
Query: "elastcisearch" (Length 14)
            │
  [ Transposition: 'ci' -> 'ic' (1 edit) ]
            │
            ▼
Index Term: "elasticsearch" ──► Match! (Distance = 1 <= AUTO limit 2)
```

## Build it
See `code/levenshtein_demo.py` implementing Levenshtein edit distance in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/19-fuzzy-search/experiments/run_experiment.sh
```

## Inspect it
Test fuzzy matching on misspelled query:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "fuzzy": {
      "title": { "value": "ergnomic", "fuzziness": "AUTO" }
    }
  }
}'
```

## Measure it
Notice query latency: expanding fuzzy terms builds a Levenshtein automaton over the term dictionary, which is slightly more expensive than exact term lookup.

## Break it
Set `fuzziness: 2` on short 3-letter words like `"cat"`. Observe false positive noise: `"cat"` matches `"car"`, `"cab"`, `"can"`, `"cap"`, `"hat"`, `"bat"`, `"rat"`.

## Recover it
Use `prefix_length: 2` (requiring the first 2 characters to match exactly before applying edits) and `fuzziness: "AUTO"`.

## Modify it
Combine fuzzy matching with `match` query: `match: { title: { query: "ergnomic chair", fuzziness: "AUTO" } }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `prefix_length` dramatically improve fuzzy query performance?
2. What is the fundamental difference between fuzzy edit distance and semantic vector search?

## Guarantees
* Fuzzy matching guarantees detection of orthographic typos within the specified edit distance.

## Non-guarantees
* Fuzzy matching cannot match phonetic variations (`phonics` vs `fonix`) or semantic synonyms (`car` vs `automobile`).

## When to use this
* User-facing search bars with keyboard input and typo risks.

## When not to use this
* Exact identifiers, serial numbers, IP addresses, or database keys.

## What comes next
In Phase 20, we learn how to expand query recall using Synonyms.
