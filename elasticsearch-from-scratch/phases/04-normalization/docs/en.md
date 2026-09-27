# Lesson 04.1: Normalization

## Motto
"Search must match intent, not typography: casing, accents, and suffixes must be reconciled."

## Problem
A user searching for `"running"` expects to find documents containing `"Run"`, `"running"`, and `"runs"`. Without token normalization, lexical mismatches cause false negatives (zero search results).

## Prediction
Will a search for `"RUNNING"` match a document containing `"Running"` if only lowercasing is applied? What if the document contains `"ran"`?

## Why this matters
Normalization bridges the gap between how authors write content and how users submit queries.

## First principles
Normalization consists of:
1. **Case folding:** Converting uppercase to lowercase (`Running` -> `running`).
2. **Stop word filtering:** Discarding high-frequency, low-information words (`the`, `is`, `at`).
3. **Stemming:** Reducing inflected words to their root stem (`running`, `runs`, `runner` -> `run`).

## Mental model
```text
Tokens: ["Running", "the", "Distributes", "Fast"]
                      │
           [ Lowercase Filter ]
                      │
        ["running", "the", "distributes", "fast"]
                      │
             [ Stop Filter ]
                      │
        ["running", "distributes", "fast"]
                      │
            [ Porter Stemmer ]
                      │
Final:  ["run", "distribut", "fast"]
```

## Build it
See `code/normalizer.py` implementing a miniature normalization pipeline in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/04-normalization/experiments/run_experiment.sh
```

## Inspect it
Test the Porter stemmer via `_analyze`:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": ["lowercase", "stemmer"],
  "text": "Running distributed systems efficiently"
}'
```

## Measure it
Compare token counts and term reduction percentage before and after normalization.

## Break it
Notice stemming over-generalization: `"organization"` and `"organ"` might stem to overlapping roots, causing surprising false positive hits.

## Recover it
Tune stemmer aggressiveness or keep original terms in a multi-field.

## Modify it
Test language-specific stemmers (e.g. `english` vs `german` vs `french`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is stemming not always desirable (e.g. searching for specific legal statutes or chemical formulas)?
2. What is the difference between lemmatization (dictionary-based) and stemming (heuristic rule-based)?

## Guarantees
* Normalization increases search recall (fewer false negatives).

## Non-guarantees
* Normalization does not guarantee 100% precision; aggressive stemming can introduce semantic drift.

## When to use this
* Standard human-readable natural language search fields.

## When not to use this
* Exact codes, UUIDs, SKUs, passwords, and case-sensitive programmatic tokens.

## What comes next
In Phase 05, we assemble Character Filters, Tokenizers, and Token Filters into the full Elasticsearch Analyzer Pipeline.
