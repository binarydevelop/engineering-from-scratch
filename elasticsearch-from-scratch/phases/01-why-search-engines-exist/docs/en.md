# Lesson 01.1: Why Search Engines Exist

## Motto
"Linear scan is O(N) in text length and document count; search engines invert the problem to O(1) term lookup."

## Problem
When searching unstructured text inside a relational database using `WHERE description LIKE '%wireless%'`, the database must read every single record and perform a substring scan. As the dataset grows to millions of rows, search latency spikes from milliseconds to tens of seconds.

## Prediction
How much does search latency increase when linearly scanning 10,000 product descriptions versus 1,000 product descriptions for a specific keyword?

## Why this matters
Traditional B-Tree indexes only index column prefixes (e.g. `LIKE 'wireless%'`). They cannot index arbitrary interior words without scanning the entire table.

## First principles
Scanning $N$ documents each containing $L$ characters takes $O(N 	imes L)$ comparisons. In contrast, an inverted index maps words to document IDs in advance, making search proportional to the number of matching documents, not total corpus size.

## Mental model
```text
Table Scan (Naive):
Doc 1: "Mechanical Keyboard"   ──> Scan text for "wireless" -> False
Doc 2: "Wireless Gaming Mouse" ──> Scan text for "wireless" -> True (Hit)
Doc 3: "Noise Cancelling Buds" ──> Scan text for "wireless" -> False
... 1,000,000 docs later ...
```

## Build it
See `code/linear_vs_index.py` which benchmarks brute-force linear scanning across simulated product descriptions.

## Use Elasticsearch
Run the experiment:
```bash
./phases/01-why-search-engines-exist/experiments/run_experiment.sh
```

## Inspect it
Observe the latency curves reported by `linear_vs_index.py`.

## Measure it
Notice how execution time scales strictly linearly $O(N)$ with document count.

## Break it
Increase corpus size to 100,000 items in Python and observe memory and CPU saturation.

## Recover it
The architectural recovery is the inverted index introduced in Phase 02.

## Modify it
Add multi-word search (`wireless AND ergonomic`) to the linear scanner and observe how complexity multiplies.

## Evidence
Record measurements in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can a relational B-Tree index accelerate `LIKE 'abc%'` but not `LIKE '%abc%'`?
2. What is read amplification in disk-based table scans?

## Guarantees
* Linear scan guarantees complete recall if run to completion.

## Non-guarantees
* Linear scan provides zero scalability for interactive search queries.

## When to use this
* Linear scan is only acceptable for tiny collections (< 100 small items).

## When not to use this
* Any user-facing search application with more than a few hundred documents.

## What comes next
In Phase 02, we construct an Inverted Index from scratch to achieve sub-millisecond term lookup.
