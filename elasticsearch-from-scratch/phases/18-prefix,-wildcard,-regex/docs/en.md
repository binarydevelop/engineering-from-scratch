# Lesson 18.1: Prefix, Wildcard, Regex

## Motto
"Leading wildcards turn O(log M) index lookups into full dictionary scans."

## Problem
Users want to search for partial words (`*search*` or `elasti*`). Running broad wildcards against large indices causes severe CPU spikes on coordinating nodes and can crash cluster performance.

## Prediction
Why is querying `"elasti*"` vastly faster than querying `"*search*"` against an inverted index?

## Why this matters
Lucene stores terms in a sorted lexicographical dictionary (an FST or Finite State Transducer). Prefix queries can jump directly to the prefix range ($O(\log M)$). Leading wildcards force Lucene to iterate through every single term in the entire index!

## First principles
* **Prefix (`prefix: "ela"`):** Range scan across sorted term dictionary: `["ela" ... "elb")`. Extremely fast.
* **Trailing Wildcard (`wildcard: "ela*"`):** Compiled to prefix automaton. Fast.
* **Leading Wildcard (`wildcard: "*search*"`):** Must test automaton against all $M$ terms in the dictionary. Very expensive.

## Mental model
```text
Sorted Term Dictionary:
["apple", "banana", "cat", "dog", "elastic", "elasticsearch", "elephant", "zebra"]

Prefix Query "ela*":
  Binary search to "elastic" ──► Read until "elephant" ──► STOP. (Checked 2 terms)

Leading Wildcard "*search*":
  Test "apple" (No)
  Test "banana" (No)
  Test "cat" (No)
  ... Must test all 10,000,000 terms in index!
```

## Build it
See `code/prefix_wildcard_bench.py` demonstrating dictionary traversal costs.

## Use Elasticsearch
Run the experiment:
```bash
./phases/18-prefix,-wildcard,-regex/experiments/run_experiment.sh
```

## Inspect it
Test prefix query vs wildcard:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": { "prefix": { "category": "elec" } }
}'
```

## Measure it
Compare execution latency of prefix query vs broad regex query across 10,000 terms.

## Break it
Execute a query with multiple leading wildcards (`*a*b*c*`) across an unindexed field and observe high CPU consumption.

## Recover it
Enforce `index_prefixes` or `wildcard` field type (uses n-gram index structures to accelerate interior matching).

## Modify it
Use the `wildcard` field type (introduced in modern Elasticsearch) which indexes 3-grams to allow fast interior wildcards.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is a leading wildcard (`*term`) fundamentally incompatible with standard B-Tree or FST indexing?
2. What does Elasticsearch do if a wildcard matches more than 10,000 unique terms?

## Guarantees
* Trailing prefix queries execute in logarithmic time relative to term dictionary size.

## Non-guarantees
* Leading wildcards on standard text fields provide zero scalability.

## When to use this
* Prefix lookups for search-as-you-type, structured code prefixes, and SKU matching.

## When not to use this
* Leading wildcards on large production text fields without the dedicated `wildcard` field type.

## What comes next
In Phase 19, we explore typo tolerance using Fuzzy Search (Levenshtein edit distance).
