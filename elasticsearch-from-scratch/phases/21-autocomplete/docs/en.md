# Lesson 21.1: Autocomplete

## Motto
"Autocomplete requires sub-10ms response: compare prefix queries, edge n-grams, and completion suggesters."

## Problem
As a user types every keystroke (`e`, `el`, `ela`, `elas`), the frontend issues an HTTP query. If the backend takes 100ms per query, typing feels sluggish and drops keystrokes.

## Prediction
Which autocomplete technique offers the lowest memory overhead: live prefix queries, edge n-grams, or completion suggesters?

## Why this matters
Search-as-you-type UX demands extreme low latency (< 15ms). Three architectures exist in Elasticsearch:
1. **Prefix Query:** Zero index overhead, but executes a dictionary range scan on every keystroke.
2. **Edge N-Grams:** Generates prefix tokens at index time (`elas` -> `e`, `el`, `ela`, `elas`). Fast term lookups, larger index disk size.
3. **Completion Suggester:** In-memory FST (Finite State Transducer). Sub-millisecond speed, strictly prefix-only, consumes JVM heap.

## Mental model
```text
Approach 1: Prefix Query
  Query: "ela*" ──► Lucene scans term dictionary dynamically at search time

Approach 2: Edge N-Grams (Index Time)
  "elastic" ──► Indexed as ["e", "el", "ela", "elas", "elast", "elasti", "elastic"]
  Query: "ela" ──► Standard O(1) inverted index exact term lookup!

Approach 3: Completion Suggester
  In-memory FST in JVM heap ──► Traversing state machine (sub-millisecond)
```

## Build it
See `code/autocomplete_compare.py` contrasting edge n-grams against prefix scanning in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/21-autocomplete/experiments/run_experiment.sh
```

## Inspect it
Create a completion suggester index and issue a suggestion request:
```bash
curl -X POST http://localhost:9200/suggest_demo/_search -H "Content-Type: application/json" -d '{
  "suggest": {
    "product_suggest": {
      "prefix": "mech",
      "completion": { "field": "suggest" }
    }
  }
}'
```

## Measure it
Compare latency: Completion Suggester (< 2ms) vs Edge N-gram (< 8ms) vs Wildcard (> 30ms).

## Break it
Load 5,000,000 suggestions into completion suggester and observe JVM heap memory consumption.

## Recover it
Switch to disk-backed Edge N-grams if suggestions exceed available JVM heap.

## Modify it
Add context suggesters (e.g. autocomplete restricted by user location or category).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is the Completion Suggester stored in JVM heap memory rather than disk?
2. What are the trade-offs between Edge N-grams and Completion Suggesters?

## Guarantees
* Completion suggesters guarantee near-instant prefix matching.

## Non-guarantees
* Standard completion suggesters cannot match words in the middle of a string (prefix only).

## When to use this
* Search bar suggestion dropdowns with strict latency budgets.

## When not to use this
* Deep interior text search across document bodies.

## What comes next
In Phase 22, we analyze index size explosion caused by N-grams.
