# Lesson 06.1: Documents and Fields

## Motto
"A document is not a blob; it is a dictionary of fields, each demanding its own indexing strategy."

## Problem
Real-world entities have diverse attributes: a title requires full-text stemming, a price requires numeric range filtering, a category requires exact grouping, and a date requires chronological slicing. Indexing everything as raw text breaks range queries and sorting.

## Prediction
If you index `price: 499` as text, will a range query for prices between 50 and 100 correctly exclude 499, or will string collation treat `"499"` as smaller than `"50"`?

## Why this matters
Treating all fields as identical text strings destroys query correctness. String sorting compares character ASCII codes (`"499" < "50"`), whereas numeric sorting compares numerical magnitudes.

## First principles
An Elasticsearch index contains multiple Lucene field structures per document:
* Inverted index for `text` fields
* BKD trees (multidimensional points) for `integer`, `float`, and `date`
* Columnar doc values for `keyword` and numbers

## Mental model
```text
Document:
{
  "title": "Ergonomic Chair",       ──► Inverted Index ("ergonom", "chair")
  "price": 299.99,                  ──► BKD Tree Point (299.99)
  "category": "furniture",          ──► Doc Values & Exact Postings ("furniture")
  "in_stock": true                  ──► 1-bit boolean structure
}
```

## Build it
See `code/fielded_search.py` demonstrating per-field indexing and fielded search in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/06-documents-and-fields/experiments/run_experiment.sh
```

## Inspect it
Index a document and inspect its stored representation:
```bash
curl -X PUT http://localhost:9200/products_demo/_doc/1 -H "Content-Type: application/json" -d '{
  "title": "Ergonomic Office Chair",
  "price": 299.99,
  "category": "furniture",
  "in_stock": true
}'
curl -s http://localhost:9200/products_demo/_doc/1?pretty
```

## Measure it
Compare search response time when searching against a specific field (`title:chair`) vs all fields.

## Break it
Try to run a numeric range filter on a field that was indexed as text.

## Recover it
Define an explicit mapping specifying numeric data types.

## Modify it
Add a new nested object field and inspect how Elasticsearch infers its structure.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does lexicographical string sorting fail for numbers (`"10"` vs `"2"`)?
2. How does Lucene physically store different field types on disk?

## Guarantees
* Each field maintains its own isolated indexing structures tailored to its type.

## Non-guarantees
* Elasticsearch does not enforce relational foreign key constraints between documents.

## When to use this
* Every structured JSON entity stored in Elasticsearch.

## When not to use this
* Unstructured binary blobs (store them in S3/blob store, index only their extracted metadata).

## What comes next
In Phase 07, we explore the fundamental distinction between `text` and `keyword` field types.
