# Lesson 32.1: Doc Values

## Motto
"Inverted indexes map terms to documents; doc values map documents to terms in a disk-backed columnar format."

## Problem
An inverted index answers: *"Which documents contain 'electronics'?"*
Sorting or aggregating answers the opposite: *"What is the value of 'price' for Document 42, 88, 91, and 104?"*
Extracting values from an inverted index requires un-inverting it into memory. Doing that across millions of hits exhausts JVM heap.

## Prediction
Why are doc values stored on disk and memory-mapped by the OS, rather than loaded into the JVM garbage-collected heap?

## Why this matters
Doc Values make sorting, aggregations, and script execution scalable. By keeping them in the OS page cache, Lucene avoids JVM garbage collection pauses.

## First principles
* **Inverted Index (Row to Term):**
  `Term -> [Doc 1, Doc 4, Doc 9]`
* **Doc Values (Columnar):**
  `Doc 1 -> 45.0`
  `Doc 2 -> 19.99`
  `Doc 3 -> 120.0`
Stored in Lucene `.dvd` (doc values data) and `.dvm` (doc values metadata) files.

## Mental model
```text
Row-Oriented (_source):
  Doc 1: { title: "A", price: 10, cat: "tech" }
  Doc 2: { title: "B", price: 20, cat: "home" }

Columnar (Doc Values):
  PRICE Column: [Doc 1: 10, Doc 2: 20, Doc 3: 15, Doc 4: 90]
  Sort/Aggregation reads contiguous bytes sequentially from disk page cache!
```

## Build it
See `code/columnar_doc_values_sim.py` demonstrating row-to-column iteration speeds in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/32-doc-values/experiments/run_experiment.sh
```

## Inspect it
Check segment files for doc values (`.dvd` and `.dvm`):
```bash
curl -s "http://localhost:9200/_cat/segments/products_phase06?v" | grep -E 'dvd|dvm' || true
```

## Measure it
Compare aggregation execution time on fields with doc values enabled vs disabled.

## Break it
Disable doc values on a keyword field (`"doc_values": false`) and attempt to sort by that field:
`"Field [category] of type [keyword] does not support doc_values"`

## Recover it
Doc values are enabled by default on all `keyword`, numeric, date, and boolean fields. Only disable them if you will NEVER sort, aggregate, or script on that field.

## Modify it
Inspect doc values compression algorithms (Lucene uses bit-packing and table-based encodings).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does storing doc values outside the JVM heap protect the cluster from GC pauses?
2. Why are doc values disabled by default on analyzed `text` fields?

## Guarantees
* Doc values provide high-throughput sequential columnar scans for aggregations.

## Non-guarantees
* Doc values cannot perform fast full-text term lookups (that is the job of the inverted index).

## When to use this
* Every field used in `aggs`, `sort`, or painless scripts.

## When not to use this
* Fields that are strictly searched and never sorted or aggregated (set `doc_values: false` to save disk).

## What comes next
In Phase 33, we inspect Fielddata: the in-memory hazard of aggregating analyzed text.
