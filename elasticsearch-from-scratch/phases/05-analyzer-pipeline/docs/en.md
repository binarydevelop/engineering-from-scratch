# Lesson 05.1: Analyzer Pipeline

## Motto
"An analyzer is a three-stage factory: Character Filters mutate chars, Tokenizer emits tokens, Token Filters refine tokens."

## Problem
In production, documents arrive containing dirty HTML markup (`<p>Hello &amp; welcome</p>`), mixed character encodings, and abbreviations. If tokenization occurs before stripping HTML tags, the tags themselves become inverted index terms.

## Prediction
If you process `"<p>Elasticsearch &amp; Lucene</p>"` through a standard analyzer without a character filter, will `p` and `amp` be indexed as terms?

## Why this matters
Understanding the strict 3-stage hierarchy enables designing custom analyzers for e-commerce, legal docs, code repositories, or multilingual catalogs.

## First principles
The analysis pipeline executes strictly in order:
1. **Character Filters (0 or more):** Receive raw characters, emit transformed characters.
2. **Tokenizer (exactly 1):** Receives characters, emits token stream.
3. **Token Filters (0 or more):** Receive tokens, emit modified/filtered tokens.

## Mental model
```text
Raw String: "<b>High-Performance</b> &amp; Fast!"
                    │
   [ Char Filter 1: html_strip ]
                    ▼
            "High-Performance &amp; Fast!"
                    │
   [ Char Filter 2: mapping (&amp; -> and) ]
                    ▼
            "High-Performance and Fast!"
                    │
   [ Tokenizer: standard ]
                    ▼
         ["High", "Performance", "and", "Fast"]
                    │
   [ Token Filter 1: lowercase ]
                    ▼
         ["high", "performance", "and", "fast"]
                    │
   [ Token Filter 2: stop ]
                    ▼
         ["high", "performance", "fast"]
```

## Build it
See `code/custom_analyzer_test.py` simulating the three distinct stages.

## Use Elasticsearch
Run the experiment:
```bash
./phases/05-analyzer-pipeline/experiments/run_experiment.sh
```

## Inspect it
Use the `_analyze` API with inline custom components:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "char_filter": ["html_strip"],
  "tokenizer": "standard",
  "filter": ["lowercase", "stop"],
  "text": "<h1>Elasticsearch</h1> is <b>fast</b>!"
}'
```

## Measure it
Inspect token start and end character offsets to see how `html_strip` preserves original character positions for highlighting.

## Break it
Put a token filter before a tokenizer—observe that Elasticsearch rejects the configuration at index creation because the pipeline order is immutable.

## Recover it
Respect the invariant: `char_filter -> tokenizer -> filter`.

## Modify it
Add a synonym filter to the token filter chain.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can an analyzer have multiple character filters and token filters, but only exactly ONE tokenizer?
2. What happens if the query-time analyzer differs from the index-time analyzer?

## Guarantees
* Analysis is deterministic: identical text fed to identical analyzer configs always produces identical terms.

## Non-guarantees
* Analysis cannot reconstruct the original text formatting once terms are emitted.

## When to use this
* Every full-text search field requires a conscious analyzer design.

## When not to use this
* Do not apply analyzers to exact values like UUIDs or IP addresses.

## What comes next
In Phase 06, we move from individual strings to structured JSON documents with heterogeneous fields.
