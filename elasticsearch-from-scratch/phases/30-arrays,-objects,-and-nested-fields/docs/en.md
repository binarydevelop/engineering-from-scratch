# Lesson 30.1: Arrays, Objects, and Nested Fields

## Motto
"Lucene has no concept of inner objects: standard arrays of objects are flattened into parallel lists, causing false cross-object matches."

## Problem
You index a document with an array of people:
`[{"first": "Alice", "last": "Smith"}, {"first": "Bob", "last": "Jones"}]`
You query for `first: "Alice" AND last: "Jones"`.
**Surprise:** Standard Elasticsearch returns a HIT! Why did Alice match Bob's last name?

## Prediction
Why does standard JSON object array indexing in Lucene correlate Alice with Jones?

## Why this matters
This is a mandatory lesson. Apache Lucene does NOT have inner objects. In standard indexing, it flattens the document into two independent parallel arrays:
* `user.first = ["Alice", "Bob"]`
* `user.last = ["Smith", "Jones"]`
The relationship between Alice and Smith is completely erased!

## First principles
* **Standard Object Flattening:** Destroys intra-object correlation.
* **`nested` Field Type:** Indexes each inner object as a **hidden separate Lucene document** connected to the parent document via a block join.
* **`nested` Query:** Enforces that boolean criteria must match within the boundary of a single nested child document!

## Mental model
```text
Standard Flattening (Broken Correlation):
  Doc 1:
    user.first = ["Alice", "Bob"]
    user.last  = ["Smith", "Jones"]
  Query (first: Alice AND last: Jones) ──► MATCH! (False Positive!)

Nested Document Architecture (Preserves Correlation):
  Parent Doc 1
    ├── Child Doc 1.1: { first: "Alice", last: "Smith" }
    └── Child Doc 1.2: { first: "Bob",   last: "Jones" }
  Query: first: Alice AND last: Jones ──► REJECTED! (Neither child matches both)
```

## Build it
See `code/flattened_vs_nested_demo.py` showing false cross-object matches in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/30-arrays,-objects,-and-nested-fields/experiments/run_experiment.sh
```

## Inspect it
Create an index with `type: nested` and compare queries:
```bash
curl -X PUT http://localhost:9200/nested_users -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "users": { "type": "nested" }
    }
  }
}'
```

## Measure it
Notice segment document count: each parent document with $N$ nested objects consumes $1 + N$ Lucene documents!

## Break it
Index a document with 10,000 nested items and watch it hit the `index.mapping.nested_objects.limit` safety threshold.

## Recover it
Flatten nested objects or model them as independent parent-child documents or separate indices.

## Modify it
Query using the `nested` query block:
```json
{
  "query": {
    "nested": {
      "path": "users",
      "query": {
        "bool": {
          "must": [
            { "match": { "users.first": "Alice" } },
            { "match": { "users.last": "Smith" } }
          ]
        }
      }
    }
  }
}
```

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does standard object mapping in Elasticsearch lose the connection between fields of an inner object?
2. How does Lucene physically store `nested` documents on disk?

## Guarantees
* `nested` queries guarantee that all query clauses match within the same child object boundary.

## Non-guarantees
* `nested` does not scale to unbounded arrays (e.g. hundreds of thousands of child items per parent).

## When to use this
* Arrays of structured objects where multi-field correlation is required (order line items, author lists).

## When not to use this
* Simple primitive arrays (`tags: ["apple", "banana"]`), or read-only display blobs.

## What comes next
In Phase 31, we compare `_source`, stored fields, and indexed terms.
