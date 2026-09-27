# Lesson 07.1: text vs keyword

## Motto
"Text is for searching inside; keyword is for filtering, sorting, and aggregating exactly."

## Problem
Engineers frequently map a status field (`"Order In Progress"`) as `text` and wonder why sorting fails or aggregations return separate buckets for `"order"`, `"in"`, and `"progress"`. Conversely, they map product titles as `keyword` and wonder why searching for a single word returns zero hits.

## Prediction
If a field is mapped as `text`, will a `term` query for `"United States"` match a document where `country: "United States"`? Why or why not?

## Why this matters
This is the single most common mapping mistake in Elasticsearch. `text` enables full-text search via inverted index of analyzed tokens. `keyword` enables exact filtering, sorting, and aggregations via columnar doc values.

## First principles
* **`text`:** Analyzed. `United States` -> tokens `["united", "states"]`. Stored in inverted index.
* **`keyword`:** Verbatim. `United States` -> exact term `"United States"`. Stored in inverted index and Doc Values.
* **Multi-field (`fields`):** Indexes a single field both ways! `title` (text) and `title.keyword` (keyword).

## Mental model
```text
Raw String: "Distributed Systems"

             ┌────────────────────────────────────────────────────────┐
             │                     MAPPING DECISION                   │
             └────────────────────────────────────────────────────────┘
                           │                                  │
          Mapped as "text" │                 Mapped as "keyword"
                           ▼                                  ▼
                Analyzed via Standard               Indexed Verbatim
               ["distributed", "systems"]          ["Distributed Systems"]
                           │                                  │
       Used for: match queries & relevance       Used for: term filters, sort, aggs
```

## Build it
See `code/text_vs_keyword_demo.py` contrasting tokenized vs verbatim lookup.

## Use Elasticsearch
Run the experiment:
```bash
./phases/07-text-vs-keyword/experiments/run_experiment.sh
```

## Inspect it
Observe the difference between `match` on `title` and `term` on `title.keyword`:
```bash
curl -X POST http://localhost:9200/demo_types/_search -H "Content-Type: application/json" -d '{
  "query": { "term": { "country.keyword": "United States" } }
}'
```

## Measure it
Compare aggregation memory: aggregating on `keyword` uses zero heap (reads disk-backed doc values), whereas aggregating on `text` requires expensive in-memory fielddata.

## Break it
Attempt to aggregate or sort on a pure `text` field. Observe the immediate failure:
`"Fielddata is disabled on text fields by default. Set fielddata=true..."`

## Recover it
Change the aggregation to target the `.keyword` multi-field instead.

## Modify it
Add custom normalizers to keyword fields (e.g. lowercase without token splitting).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a `term` query for `"United States"` against a standard analyzed `text` field return 0 results?
2. When should a field be mapped ONLY as `keyword`, and when should it be a multi-field?

## Guarantees
* `keyword` fields preserve the exact character sequence without tokenization.

## Non-guarantees
* `keyword` fields cannot match partial interior words without expensive wildcard operations.

## When to use this
* `keyword`: Statuses, IDs, tags, enum values, URLs, postal codes, and email addresses.
* `text`: Titles, articles, descriptions, comments, and messages.

## When not to use this
* Never use `text` for fields that will be sorted or aggregated.

## What comes next
In Phase 08, we dive into explicit schema definition: Mappings.
