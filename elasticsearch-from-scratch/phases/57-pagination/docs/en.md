# Lesson 57.1: Pagination

## Motto
"from + size is O(N) in depth: deep pagination forces every shard to score and sort N documents only to discard them."

## Problem
A user jumps to Page 1,000 using `{"from": 10000, "size": 10}`. On an index with 5 shards, each of the 5 shards must collect, score, and sort 10,010 documents (50,050 total candidates), send them to the coordinator, and the coordinator sorts 50,050 items only to return 10. The coordinator runs out of memory and crashes!

## Prediction
What default safety error does Elasticsearch return if `from + size > 10000`?

## Why this matters
Deep pagination is an exponential killer of search clusters. Understanding `search_after` is mandatory for scalable pagination.

## First principles
* **`from + size`:** Offsets results. Cost is $O(	ext{from} + 	ext{size})$. Discards everything before `from`.
* **`index.max_result_window`:** Defaults to **10,000**. Protects the cluster from deep paging crashes.
* **`search_after`:** Cursor-based pagination. Uses the sort values of the last document on the current page to start the next page in $O(	ext{size})$ time, without skipping!

## Mental model
```text
from: 10,000, size: 10:
  Coordinator sorts 10,010 documents ──► Discards first 10,000 ──► Extreme Waste!

search_after: [149.99, "doc_999"]:
  Shards jump directly to items WHERE (price <= 149.99 AND id > doc_999) ──► Reads ONLY 10 items!
```

## Build it
See `code/deep_pagination_bench.py` contrasting `from` offsets vs cursor iteration in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/57-pagination/experiments/run_experiment.sh
```

## Inspect it
Test `from + size` up to the safety window:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "from": 10001,
  "size": 10
}'
```
Read the `illegal_argument_exception`: `"Result window is too large..."`.

## Measure it
Compare latency: page 1 vs page 500 using `from` vs `search_after`.

## Break it
Increase `index.max_result_window: 1000000` and query page 50,000 to watch JVM heap exhaustion.

## Recover it
Keep `max_result_window: 10000` and implement cursor pagination using `search_after`.

## Modify it
Use `search_after` with sort on `["price", "_id"]`:
```json
{
  "size": 10,
  "sort": [ { "price": "desc" }, { "_id": "asc" } ],
  "search_after": [ 149.99, "1042" ]
}
```

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `from: 50000, size: 10` force every shard to score 50,010 documents?
2. Why must `search_after` always include a tie-breaker field (like `_id`) in the sort?

## Guarantees
* `search_after` executes page $N$ with the same constant speed as page 1.

## Non-guarantees
* `search_after` does not allow jumping directly to arbitrary arbitrary distant page numbers (e.g. "Jump to page 47").

## When to use this
* Infinite scroll feeds, web scrapers, data exports, and deep result browsing.

## When not to use this
* Simple top-10 search results where `from: 0` is all that is needed.

## What comes next
In Phase 58, we stabilize pagination across concurrent updates using Point in Time (PIT).
