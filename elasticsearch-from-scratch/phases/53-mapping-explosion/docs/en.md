# Lesson 53.1: Mapping Explosion

## Motto
"A mapping explosion occurs when arbitrary user keys become schema fields, ballooning cluster state and crashing the master node."

## Problem
A developer indexes analytics events using the user ID as a JSON key:
`{"user_12345": {"clicked": true}}`
After 100,000 unique users, the index has 100,000 unique fields! The cluster state balloons to 150 MB, master nodes experience 30-second GC pauses, and the entire cluster stops responding to queries.

## Prediction
What safety limit does Elasticsearch enforce on the maximum number of fields in an index?

## Why this matters
Mapping explosions are among the most catastrophic production outages. Once fields enter a mapping, they can never be removed without reindexing!

## First principles
* Every field defined in a mapping consumes JVM heap memory in cluster state on **every single node**.
* Lucene segments allocate data structures per field. Having 20,000 fields per document ruins indexing and search performance.
* Safety Setting: `index.mapping.total_fields.limit` (default is **1,000 fields** in modern Elasticsearch).

## Mental model
```text
Bad Design (Dynamic User Keys):
  { "user_1": true, "user_2": true, "user_3": true... } ──► 1,000,000 FIELDS! (CRASH)

Correct Design (Key-Value Array or Flattened Type):
  { "users": ["user_1", "user_2", "user_3"] }          ──► EXACTLY 1 FIELD! (HEALTHY)
```

## Build it
See `code/mapping_explosion_sim.py` demonstrating field accumulation and prevention.

## Use Elasticsearch
Run the experiment:
```bash
./phases/53-mapping-explosion/experiments/run_experiment.sh
```

## Inspect it
Check field count in an index mapping:
```bash
curl -s http://localhost:9200/products_phase06/_mapping | grep -o '"type":' | wc -l
```

## Measure it
Inspect cluster state memory growth during field additions.

## Break it
Index documents with dynamically generated field names until exceeding the default limit:
`"Limit of total fields [1000] has been exceeded"`

## Recover it
1. Use `type: "flattened"` for arbitrary JSON blobs (indexes keys without creating cluster state fields!).
2. Redesign document model: store arbitrary attributes as an array of key-value pairs:
   `[{"key": "color", "value": "blue"}, {"key": "size", "value": "XL"}]`.

## Modify it
Inspect `flattened` field type in modern Elasticsearch.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having 50,000 fields destabilize the elected master node?
2. How does the `flattened` data type prevent mapping explosions?

## Guarantees
* `index.mapping.total_fields.limit` strictly blocks writes that would cause mapping explosions.

## Non-guarantees
* Raising the limit arbitrarily (`10000`) does not make it safe; it delays the crash.

## When to use this
* Schema review, dynamic payload ingestion, and user-generated metadata modeling.

## When not to use this
* Arbitrary dynamic JSON keys.

## What comes next
In Phase 54, we study High Cardinality fields and their memory footprint.
