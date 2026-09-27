# Lesson 20.1: Synonyms

## Motto
"A search engine must know that laptops are notebooks, but synonyms at index-time cannot be changed without reindexing."

## Problem
A retailer lists products as `"notebook computer"`. A customer searches for `"laptop"`. Because the tokens share zero lexical characters, the customer gets zero results and leaves the site.

## Prediction
If you configure synonyms at index time and later add a new synonym rule, will existing indexed documents automatically match the new synonym without reindexing?

## Why this matters
Synonyms bridge vocabulary mismatch between content creators and search users.

## First principles
Two architectures for synonyms:
1. **Index-Time Synonyms:** When indexing `"laptop"`, expand tokens to `["laptop", "notebook"]`.
   * *Pro:* Fast search.
   * *Con:* Changing synonyms requires complete reindexing; index size grows.
2. **Search-Time Synonyms (Preferred):** Keep index clean. When query for `"laptop"` arrives, expand query to `laptop OR notebook` using `synonym_graph` token filter.
   * *Pro:* Instant updates without reindexing.
   * *Con:* Slightly higher query parsing complexity.

## Mental model
```text
Index-Time:
  "laptop" ──► Indexed as ["laptop", "notebook"] into Lucene segments (Fixed forever)

Search-Time (Synonym Graph):
  Query: "buy laptop" ──► Expanded to "buy (laptop OR notebook)" at search runtime
```

## Build it
See `code/synonym_expander.py` simulating graph expansion of synonyms in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/20-synonyms/experiments/run_experiment.sh
```

## Inspect it
Test `synonym_graph` via `_analyze`:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": [
    { "type": "synonym_graph", "synonyms": ["laptop, notebook => laptop, notebook"] }
  ],
  "text": "portable laptop"
}'
```

## Measure it
Notice that synonym tokens share the exact same `position` as the original word!

## Break it
Create circular or ambiguous multi-word synonyms (e.g. `"fast, quick"` and `"quick fix"`) and observe phrase query graph distortion.

## Recover it
Always use `synonym_graph` token filter at search time for multi-word synonyms.

## Modify it
Test directional synonyms (`"macbook => apple, laptop"`) versus equivalent synonyms (`"laptop, notebook"`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is applying synonyms at search time generally preferred over index time?
2. Why must multi-word synonyms use `synonym_graph` instead of standard `synonym` filter?

## Guarantees
* Synonyms expand query candidate matching across equivalent domain vocabularies.

## Non-guarantees
* Synonyms do not automatically handle polysemy (words with multiple meanings, e.g. "apple" fruit vs company).

## When to use this
* Domain terminologies, acronyms (`AI, artificial intelligence`), and localized vocabulary.

## When not to use this
* Huge unfiltered synonym dictionaries that explode query term counts and dilute relevance.

## What comes next
In Phase 21, we design fast Autocomplete systems.
