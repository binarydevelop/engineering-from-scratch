#!/usr/bin/env python3
"""
build_curriculum_part2.py - Generates Phases 11 to 25 for elasticsearch-from-scratch.
Covers Boolean queries, Query vs Filter, BM25, Phrase Search, Autocomplete, Geo, etc.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(BASE_DIR, "phases")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    if path.endswith(".sh") or path.endswith(".py"):
        os.chmod(path, 0o755)

def evidence_template(phase_title, phase_num):
    return f"""# Evidence Log: Phase {phase_num:02d} - {phase_title}

Date: 2026-09-23
Elasticsearch Version: 8.17.0
Lucene Version: 9.12.0
Working Directory: phases/{phase_num:02d}-{phase_title.lower().replace(' ', '-').replace('/', '-')}

## Prediction
Before executing the experiment, record your hypothesis here:

## Commands Executed
```bash
./experiments/run_experiment.sh
```

## Important Terminal Output
```text
```

## Measurements
* Metric 1:
* Metric 2:

## What Actually Happened?

## What Did I Intentionally Break?

## How Did I Diagnose It?

## How Did I Recover?

## Explain the Concept in My Own Words:
"""

def generate_phases_11_to_25():
    phases = [
        (11, "Boolean Search",
         "Boolean queries are set algebra with relevance: must intersects, should boosts, filter excludes scoring, must_not inverts.",
         """# Lesson 11.1: Boolean Search

## Motto
"Boolean queries are set algebra with relevance: must intersects, should boosts, filter excludes scoring, must_not inverts."

## Problem
Users rarely search for single words. They want: "wireless keyboard, under $100, preferably mechanical, but NOT refurbished". Representing this in search requires combining multiple independent clauses with distinct scoring rules.

## Prediction
In a `bool` query, does a clause in the `should` section require a document to match if `must` clauses are already present?

## Why this matters
The `bool` query is the workhorse of Elasticsearch query composition. Almost every production search query is wrapped in a `bool` container.

## First principles
The four clauses of `bool`:
* `must`: Logical AND. Document MUST match. Score is added to total score.
* `filter`: Logical AND. Document MUST match. Score is ignored ($0.0$). Results are cached.
* `should`: Logical OR / Boost. If `must` is present, `should` acts as an optional score booster. If no `must` is present, at least one `should` clause must match (`minimum_should_match: 1`).
* `must_not`: Logical NOT. Document MUST NOT match. Executed in filter context.

## Mental model
```text
                    BOOL QUERY
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
   MUST              FILTER            SHOULD
 (Intersection)    (Binary Check)   (Score Booster)
 (Affects Score)   (Score = 0.0)    (Optional if Must)
```

## Build it
See `code/bool_search.py` implementing `must`, `should`, and `must_not` over postings lists.

## Use Elasticsearch
Run the experiment:
```bash
./phases/11-boolean-search/experiments/run_experiment.sh
```

## Inspect it
Test `bool` with must, filter, and should:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "must": [{ "match": { "title": "keyboard" } }],
      "filter": [{ "range": { "price": { "lte": 150 } } }],
      "should": [{ "match": { "title": "mechanical" } }],
      "must_not": [{ "term": { "category": "furniture" } }]
    }
  }
}'
```

## Measure it
Compare scoring breakdown: documents matching the `should` clause receive higher scores than documents matching only `must`.

## Break it
Set `minimum_should_match: 2` when only 1 should clause exists and observe zero hits.

## Recover it
Align `minimum_should_match` with available should clauses.

## Modify it
Add `boost: 2.0` to the `should` clause and observe ranking reordering.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `filter` improve query speed compared to `must`?
2. When does a `should` clause become mandatory?

## Guarantees
* `bool` enforces exact boolean set logic across all clauses.

## Non-guarantees
* `bool` does not prevent slow execution if interior clauses contain unindexed wildcards.

## When to use this
* Standard application search forms with multiple filters and keywords.

## When not to use this
* Simple single-term exact lookups (use a single `term` query directly).

## What comes next
In Phase 12, we measure the performance and scoring differences between Query Context and Filter Context.
""",
"""#!/usr/bin/env python3

def boolean_search(docs, must_terms=None, filter_fn=None, should_terms=None, must_not_terms=None):
    must_terms = must_terms or []
    should_terms = should_terms or []
    must_not_terms = must_not_terms or []
    results = []

    for doc_id, doc in docs.items():
        text = doc.get("text", "").lower()
        # 1. Check must_not
        if any(term in text for term in must_not_terms):
            continue
        # 2. Check must
        if not all(term in text for term in must_terms):
            continue
        # 3. Check filter
        if filter_fn and not filter_fn(doc):
            continue
        # 4. Calculate score (must + should boosts)
        score = len(must_terms) * 1.0
        for st in should_terms:
            if st in text:
                score += 1.5
        results.append((doc_id, score, doc))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

if __name__ == "__main__":
    catalog = {
        1: {"text": "mechanical wireless keyboard", "price": 120},
        2: {"text": "membrane quiet keyboard", "price": 40},
        3: {"text": "refurbished mechanical keyboard", "price": 70},
        4: {"text": "ergonomic wireless mouse", "price": 60}
    }
    hits = boolean_search(
        catalog,
        must_terms=["keyboard"],
        filter_fn=lambda d: d["price"] <= 130,
        should_terms=["mechanical"],
        must_not_terms=["refurbished"]
    )
    print("Boolean Search Results:")
    for doc_id, score, doc in hits:
        print(f"  Doc {doc_id} (Score: {score:.1f}): {doc}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 11: Boolean Query Experiments ==="
python3 phases/11-boolean-search/code/11_boolean_search.py
"""),

        (12, "Query vs Filter",
         "Queries score relevance; filters ask binary existence. Filters can be cached; query scoring cannot.",
         """# Lesson 12.1: Query vs Filter

## Motto
"Queries score relevance; filters ask binary existence. Filters can be cached; query scoring cannot."

## Problem
Running structured criteria (like `status: "ACTIVE"` or `created_at > 2026-01-01`) inside query context wastes CPU calculating BM25 relevance scores on fields where relevance is meaningless, while preventing Node Query Cache reuse.

## Prediction
Will a query clause returning hits have `_score: 0.0` when placed inside the `filter` block of a `bool` query?

## Why this matters
Filter context evaluates to a bitset (0 or 1). Elasticsearch caches frequent filter bitsets in the Node Query Cache (RAM). Next time the filter executes, it costs $O(1)$ bitwise AND operations instead of scanning Lucene indexes.

## First principles
* **Query Context:** "How well does this document match?" Relevance score is calculated via BM25. Cannot be cached as a bitset because score depends on query terms and document lengths.
* **Filter Context:** "Does this document match? Yes or No." Score is fixed at $0.0$. Candidate set is cached in memory as a Roaring Bitmap.

## Mental model
```text
Query Context:
  "title: wireless" ──► Compute BM25(tf, idf, len) ──► Score: 1.452 (Not Cacheable)

Filter Context:
  "price <= 100"    ──► Binary Check (True/False)   ──► Bitset [1, 0, 1, 1] ──► CACHED!
```

## Build it
See `code/query_vs_filter_bench.py` contrasting scoring overhead against binary filtering.

## Use Elasticsearch
Run the experiment:
```bash
./phases/12-query-vs-filter/experiments/run_experiment.sh
```

## Inspect it
Observe scores returned:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "filter": [{ "term": { "category": "furniture" } }]
    }
  }
}'
```
Notice `_score: 0.0` for all hits.

## Measure it
Run repeated filter queries and inspect Node Query Cache hits via `_nodes/stats/indices/query_cache`.

## Break it
Put high-cardinality timestamps (`filter: { range: { timestamp: { gte: "now-1s" } } }`) in filters and observe cache churn.

## Recover it
Round timestamps to stable time buckets (e.g. `now/m` or `now/h`) so filter bitsets can be reused in cache.

## Modify it
Combine a scored `match` with two cached `filter` clauses.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch assign `_score: 0.0` to filter clauses?
2. How does the Node Query Cache decide which filter bitsets to keep in memory?

## Guarantees
* Filter clauses never alter document BM25 relevance ordering.

## Non-guarantees
* Putting a unique timestamp per request into a filter will not benefit from caching.

## When to use this
* Exact status flags, tenant IDs, date ranges, price filters, category facets.

## When not to use this
* When user search intent requires fuzzy, stemmed, or weighted ranking.

## What comes next
In Phase 13, we build relevance ranking from scratch, beginning with Term Frequency and Document Frequency.
""",
"""#!/usr/bin/env python3
import time
import math

def simulate_query_context(docs, term):
    # Computes scoring cost
    hits = []
    for doc_id, text in docs.items():
        count = text.lower().count(term)
        if count > 0:
            score = count * math.log(100.0)
            hits.append((doc_id, score))
    return hits

def simulate_filter_context(docs, target_category):
    # Binary bitset check
    bitset = []
    for doc_id, cat in docs.items():
        bitset.append((doc_id, 1 if cat == target_category else 0))
    return [doc_id for doc_id, matched in bitset if matched == 1]

if __name__ == "__main__":
    docs = {i: "ergonomic wireless keyboard mechanical switch" for i in range(10000)}
    categories = {i: "electronics" if i % 2 == 0 else "furniture" for i in range(10000)}

    t0 = time.perf_counter()
    for _ in range(50):
        _ = simulate_query_context(docs, "wireless")
    query_time = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    for _ in range(50):
        _ = simulate_filter_context(categories, "electronics")
    filter_time = (time.perf_counter() - t0) * 1000

    print(f"50x Query Context (Scoring): {query_time:.2f} ms")
    print(f"50x Filter Context (Bitset):  {filter_time:.2f} ms")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 12: Query vs Filter Context ==="
python3 phases/12-query-vs-filter/code/12_query_vs_filter.py
"""),

        (13, "Ranking From Scratch",
         "Searching without ranking is finding needles in haystacks without knowing which needle is sharpest.",
         """# Lesson 13.1: Ranking From Scratch

## Motto
"Searching without ranking is finding needles in haystacks without knowing which needle is sharpest."

## Problem
A search for `"database"` matches 10,000 documents. If all matching documents are returned in arbitrary insertion order, the user must browse hundreds of pages to find the most relevant document.

## Prediction
If Document A mentions `"database"` once in a 1,000-word essay, and Document B mentions `"database"` five times in a 20-word summary, which document should rank first?

## Why this matters
Search quality is defined by ranking accuracy. A search engine that returns the right document at rank 50 is functionally equivalent to broken search.

## First principles
Ranking primitives:
1. **Term Frequency (TF):** How often does the term appear in this document? (More is generally better).
2. **Document Length:** How long is the document? (A match in a short title is more specific than in an encyclopedia).
3. **Document Frequency (DF):** How common is the word across all documents?

## Mental model
```text
Doc 1: "Database internals and database architecture." (Len: 5 words, TF: 2) ──► High Density!
Doc 2: "A very long history of computing mentioning a database once..." (Len: 50 words, TF: 1) ──► Low Density
```

## Build it
See `code/naive_ranking.py` implementing match-count vs density ranking in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/13-ranking-from-scratch/experiments/run_experiment.sh
```

## Inspect it
Observe ordering differences between raw occurrence count and density-normalized scores.

## Measure it
Compare top-3 ranks under naive count vs length-normalized ranking.

## Break it
Notice keyword stuffing: an author repeats `"database database database database"` 50 times to game naive frequency ranking.

## Recover it
Apply Term Frequency Saturation (introduced in Phase 15 with BM25).

## Modify it
Add title field weighting (boost factor $2\times$) to simulate multi-field ranking.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does raw term count fail to rank documents accurately?
2. What is keyword stuffing and how does information retrieval defend against it?

## Guarantees
* Density ranking penalizes excessively verbose documents.

## Non-guarantees
* Simple density does not account for the global rarity of words.

## When to use this
* As the conceptual bridge from boolean matching to probabilistic ranking.

## When not to use this
* Production search (use modern BM25 instead).

## What comes next
In Phase 14, we introduce Inverse Document Frequency (TF-IDF intuition).
""",
"""#!/usr/bin/env python3

def naive_term_count(doc, term):
    return doc.lower().split().count(term)

def length_normalized_score(doc, term):
    words = doc.lower().split()
    tf = words.count(term)
    doc_len = len(words)
    return tf / doc_len if doc_len > 0 else 0.0

if __name__ == "__main__":
    corpus = {
        "Doc A (Short Title)": "Database systems and database design",
        "Doc B (Long Article)": "This article discusses computer hardware, networking protocols, operating systems, and a database briefly mentioned at the end of the chapter.",
        "Doc C (Keyword Stuffed)": "database database database database database"
    }

    print("Ranking for query 'database':\\n")
    print(f"{'Document':25s} | {'Raw Count':10s} | {'Length Norm Score':15s}")
    print("-" * 60)
    for title, text in corpus.items():
        raw = naive_term_count(text, "database")
        norm = length_normalized_score(text, "database")
        print(f"{title:25s} | {raw:10d} | {norm:15.4f}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 13: Ranking From Scratch ==="
python3 phases/13-ranking-from-scratch/code/13_ranking_from_scratch.py
"""),

        (14, "TF-IDF Intuition",
         "Common words carry little information; rare words carry immense signal.",
         """# Lesson 14.1: TF-IDF Intuition

## Motto
"Common words carry little information; rare words carry immense signal."

## Problem
When searching for `"the elasticsearch architecture"`, every English document contains `"the"`. If `"the"` is scored equally with `"elasticsearch"`, documents will be ranked based on how often they use stop words rather than whether they discuss Elasticsearch.

## Prediction
If a query contains two terms, one appearing in 90% of documents and one appearing in 0.1% of documents, how much more weight should the rare term receive?

## Why this matters
TF-IDF (Term Frequency-Inverse Document Frequency) established modern Information Retrieval. It mathematically formalizes the intuition of term informativeness.

## First principles
* **Term Frequency (TF):** Measures local importance within a document: $\text{TF}(t, d)$.
* **Inverse Document Frequency (IDF):** Measures global rarity across corpus:
  $$\text{IDF}(t) = \ln\left(1 + \frac{N}{\text{DF}(t)}\right)$$
  Where $N$ is total documents, and $\text{DF}(t)$ is number of documents containing term $t$.
* **Score:** $\text{TF}(t, d) \times \text{IDF}(t)$.

## Mental model
```text
Term: "the"           ──► In 10,000 of 10,000 docs ──► IDF ≈ ln(1 + 1) ≈ 0.69 (Low Signal)
Term: "elasticsearch" ──► In 5 of 10,000 docs      ──► IDF ≈ ln(1 + 2000) ≈ 7.60 (High Signal!)
```

## Build it
See `code/tfidf_scorer.py` computing TF-IDF across a multi-document corpus in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/14-tf-idf-intuition/experiments/run_experiment.sh
```

## Inspect it
Observe how matching a rare term dramatically outscores matching common terms.

## Measure it
Compare scores for multi-term queries where one term is rare and one is frequent.

## Break it
Notice what happens as term frequency in a document increases from 10 to 1,000: in classic TF-IDF, score increases linearly without bound, enabling keyword stuffing.

## Recover it
Introduce term frequency saturation (BM25 in Phase 15).

## Modify it
Vary corpus size $N$ from 100 to 1,000,000 and plot the IDF curve.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does IDF use a logarithmic scale rather than a linear scale?
2. What happens to the IDF of a term that appears in every single document in the index?

## Guarantees
* Rare terms receive exponentially higher relative weighting than common terms.

## Non-guarantees
* Classic TF-IDF does not prevent score distortion from repeated terms in long documents.

## When to use this
* As the foundational conceptual framework before understanding BM25.

## When not to use this
* Elasticsearch 8.x uses BM25 by default; do not implement raw TF-IDF manually in production.

## What comes next
In Phase 15, we implement BM25 (Best Matching 25), the default relevance engine of Elasticsearch.
""",
"""#!/usr/bin/env python3
import math
from collections import Counter

class SimpleTFIDF:
    def __init__(self, corpus):
        self.corpus = {k: v.lower().split() for k, v in corpus.items()}
        self.N = len(corpus)
        self.df = Counter()
        for words in self.corpus.values():
            for term in set(words):
                self.df[term] += 1

    def idf(self, term):
        df_val = self.df.get(term, 0)
        if df_val == 0:
            return 0.0
        return math.log(1.0 + (self.N / df_val))

    def score(self, query, doc_id):
        words = self.corpus[doc_id]
        score = 0.0
        for q in query.lower().split():
            tf = words.count(q)
            score += tf * self.idf(q)
        return score

if __name__ == "__main__":
    docs = {
        1: "the quick brown fox jumps over the lazy dog",
        2: "the distributed architecture of elasticsearch clusters",
        3: "the cat sat on the mat"
    }
    tfidf = SimpleTFIDF(docs)
    print(f"Corpus size: {tfidf.N} docs")
    print(f"IDF('the'):           {tfidf.idf('the'):.4f} (Appears in 3/3 docs)")
    print(f"IDF('elasticsearch'): {tfidf.idf('elasticsearch'):.4f} (Appears in 1/3 docs)")

    q = "the elasticsearch"
    print(f"\\nQuery: '{q}'")
    for doc_id in docs:
        s = tfidf.score(q, doc_id)
        print(f"  Doc {doc_id} score: {s:.4f}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 14: TF-IDF Scorer ==="
python3 phases/14-tf-idf-intuition/code/14_tf_idf_intuition.py
"""),

        (15, "BM25",
         "BM25 solves the two flaws of TF-IDF: it saturates term frequency and normalizes by field length.",
         """# Lesson 15.1: BM25 (Best Matching 25)

## Motto
"BM25 solves the two flaws of TF-IDF: it saturates term frequency and normalizes by field length."

## Problem
In classic TF-IDF, if a spammer repeats `"cheap flights"` 500 times in a page, their score is 500 times higher than a genuine document with 1 mention. Furthermore, a 10,000-word book naturally contains more mentions than a 50-word product description.

## Prediction
In BM25, does repeating a term 100 times give you 100x the score of mentioning it once, or does the score asymptotically approach an upper ceiling?

## Why this matters
BM25 is the default scoring algorithm in Elasticsearch 8.17.0 and Apache Lucene. Every relevance score you see in `_search` is computed by BM25.

## First principles
BM25 formula for term $q$:
$$\text{Score}(D, q) = \text{IDF}(q) \times \frac{\text{TF} \times (k_1 + 1)}{\text{TF} + k_1 \times \left(1 - b + b \times \frac{|D|}{\text{avgdl}}\right)}$$
Parameters in Elasticsearch 8.17.0:
* $k_1 = 1.2$: Controls **TF saturation**. As TF grows, the multiplier saturates at $(k_1 + 1) = 2.2$.
* $b = 0.75$: Controls **field length normalization**.
  * If $b = 1.0$, length penalty is fully applied.
  * If $b = 0.0$, document length is ignored completely.

## Mental model
```text
Score Multiplier
   ▲
2.2│                       ┌──────────────────────── Asymptotic Ceiling (k1 + 1)
   │                  . ' '
1.5│             . '
   │         . '
1.0│     . '
   │  . '
   └────────────────────────────────────────► Term Frequency (TF)
      1   2   3   4   5   10  20  50  100
```

## Build it
See `code/bm25_scorer.py` implementing the complete BM25 formula from scratch.

## Use Elasticsearch
Run the experiment:
```bash
./phases/15-bm25/experiments/run_experiment.sh
```

## Inspect it
Compare Python BM25 scores with Elasticsearch `_explain` outputs.

## Measure it
Plot the term frequency saturation curve for $\text{TF} \in [1, 50]$.

## Break it
Set $b = 0.0$ in custom similarity and observe how long, keyword-stuffed documents outrank short, concise titles.

## Recover it
Restore default $b = 0.75$.

## Modify it
Adjust $k_1$ from 1.2 to 2.0 to give more weight to repeated terms in technical documentation.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does BM25 saturate term frequency while classic TF-IDF does not?
2. What is the effect of setting parameter $b = 0$ on field length normalization?

## Guarantees
* An author cannot arbitrarily inflate relevance score by repeating a term infinitely.

## Non-guarantees
* BM25 does not understand semantic context or synonyms out of the box.

## When to use this
* Default relevance scoring for full-text search across documents and articles.

## When not to use this
* Exact matching, categorical filtering, or vector similarity.

## What comes next
In Phase 16, we dissect how to inspect and explain relevance scores using Elasticsearch's `_explain` API.
""",
"""#!/usr/bin/env python3
import math

class BM25:
    def __init__(self, corpus, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = {k: v.lower().split() for k, v in corpus.items()}
        self.N = len(corpus)
        self.doc_lens = {k: len(v) for k, v in self.corpus.items()}
        self.avgdl = sum(self.doc_lens.values()) / self.N if self.N > 0 else 1.0

        # Compute document frequencies
        self.df = {}
        for words in self.corpus.values():
            for w in set(words):
                self.df[w] = self.df.get(w, 0) + 1

    def idf(self, term):
        n = self.df.get(term, 0)
        # Lucene BM25 IDF formula
        return math.log(1.0 + (self.N - n + 0.5) / (n + 0.5))

    def score_term(self, term, doc_id):
        words = self.corpus[doc_id]
        tf = words.count(term)
        if tf == 0:
            return 0.0
        doc_len = self.doc_lens[doc_id]
        idf = self.idf(term)
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
        return idf * (numerator / denominator)

if __name__ == "__main__":
    corpus = {
        "doc1": "elasticsearch is a distributed search engine",
        "doc2": "elasticsearch elasticsearch elasticsearch distributed",
        "doc3": "redis is an in-memory caching key value database"
    }
    bm = BM25(corpus)
    print(f"Corpus avgdl: {bm.avgdl:.2f} words")
    print(f"IDF('elasticsearch'): {bm.idf('elasticsearch'):.4f}\\n")
    print("Scores for term 'elasticsearch':")
    for doc_id in corpus:
        score = bm.score_term("elasticsearch", doc_id)
        print(f"  {doc_id}: score = {score:.4f} (length = {bm.doc_lens[doc_id]})")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 15: BM25 Scoring Implementation ==="
python3 phases/15-bm25/code/15_bm25.py
"""),

        (16, "Explain Relevance",
         "Relevance is not magic; every floating point score is an audited sum of IDF, TF saturation, and length normalization.",
         """# Lesson 16.1: Explain Relevance

## Motto
"Relevance is not magic; every floating point score is an audited sum of IDF, TF saturation, and length normalization."

## Problem
In production, a stakeholder asks: *"Why did Document 42 rank higher than Document 88 for query 'gaming laptop'?"* Guessing leads to arbitrary boost tweaks that degrade overall search quality.

## Prediction
Can you determine from an API call the exact numeric contribution of term frequency versus inverse document frequency for a specific document?

## Why this matters
The `_explain` API provides complete transparency into Lucene's scoring calculation. It turns relevance debugging from guesswork into mathematical verification.

## First principles
The `_explain` response decomposes the score into a hierarchical tree:
* Top-level: sum of matching query clauses
* Each clause: `weight(title:keyword in doc_id)`
  * `idf`: calculated from doc count
  * `tf`: calculated with $k_1$ and $b$ length normalization factor

## Mental model
```text
Score: 2.451
  ├── weight(title:gaming in 42): 1.120
  │     ├── idf: 1.450
  │     └── tfNorm: 0.772 (tf=1, len=4, avgdl=6.2)
  └── weight(title:laptop in 42): 1.331
        ├── idf: 1.820
        └── tfNorm: 0.731 (tf=1, len=4, avgdl=6.2)
```

## Build it
See `code/parse_explain.py` illustrating how to parse and summarize Lucene explain trees in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/16-explain-relevance/experiments/run_experiment.sh
```

## Inspect it
Request an explain plan for a specific document ID:
```bash
curl -X POST http://localhost:9200/products_phase06/_explain/1 -H "Content-Type: application/json" -d '{
  "query": { "match": { "title": "chair" } }
}'
```

## Measure it
Notice the overhead: running `_explain` computes verbose descriptions and should never be enabled for high-QPS user queries.

## Break it
Run `explain: true` across 1,000 search results and observe response payload size jump to several megabytes.

## Recover it
Use `_explain` only on targeted single-document requests during relevance debugging.

## Modify it
Add a field boost (`title:chair^2.0`) and observe how the explain tree introduces a `boost: 2.0` multiplier node.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the explain tree show both `freq` (raw term count) and `tfNorm`?
2. Why is running `_explain` in production search endpoints dangerous?

## Guarantees
* The explain tree accounts for 100% of the mathematical score returned by `_search`.

## Non-guarantees
* `_explain` does not diagnose queries that fail to match candidate documents (zero hits).

## When to use this
* Investigating ranking anomalies and tuning weights/boosts.

## When not to use this
* Public customer-facing search APIs.

## What comes next
In Phase 17, we explore Phrase Search: matching words that appear in specific sequence.
""",
"""#!/usr/bin/env python3

def explain_bm25(term, tf, doc_len, avgdl, n_docs, doc_freq, k1=1.2, b=0.75):
    import math
    idf = math.log(1.0 + (n_docs - doc_freq + 0.5) / (doc_freq + 0.5))
    len_norm = 1.0 - b + b * (doc_len / avgdl)
    tf_norm = (tf * (k1 + 1)) / (tf + k1 * len_norm)
    total_score = idf * tf_norm

    explanation = {
        "term": term,
        "score": round(total_score, 4),
        "description": f"score({term}) = idf({idf:.4f}) * tfNorm({tf_norm:.4f})",
        "details": [
            {"description": f"idf(doc_freq={doc_freq}, n_docs={n_docs})", "value": round(idf, 4)},
            {"description": f"tfNorm(tf={tf}, doc_len={doc_len}, avgdl={avgdl:.1f})", "value": round(tf_norm, 4)}
        ]
    }
    return explanation

if __name__ == "__main__":
    tree = explain_bm25("keyboard", tf=2, doc_len=6, avgdl=8.5, n_docs=1000, doc_freq=50)
    print(f"Term: {tree['term']} | Total Score: {tree['score']}")
    print(f"Formula: {tree['description']}")
    for d in tree["details"]:
        print(f"  - {d['description']}: {d['value']}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 16: Explain Relevance ==="
python3 phases/16-explain-relevance/code/16_explain_relevance.py
"""),

        (17, "Phrase Search",
         "Words in proximity carry meaning that isolated terms lose: position matters.",
         """# Lesson 17.1: Phrase Search

## Motto
"Words in proximity carry meaning that isolated terms lose: position matters."

## Problem
Searching for `"distributed systems"` should match a book on distributed computing, but should NOT rank a document that says: *"The system was distributed across three offices and had multiple plumbing systems."* Term matching alone cannot differentiate adjacent words from words separated by 50 paragraphs.

## Prediction
Will a document containing `"distributed operating systems"` match a `match_phrase` query for `"distributed systems"` with default parameters? What about with `slop: 1`?

## Why this matters
Phrase search preserves semantic word groupings. It relies on term positions recorded in Lucene's `.pos` inverted index files.

## First principles
* **Positional Postings List:** Stores not just Doc ID, but the exact token position indices:
  `"distributed" -> [Doc 1 (pos: 0)]`
  `"systems" -> [Doc 1 (pos: 1)]`
* **Match:** Adjacent positions `pos("systems") - pos("distributed") == 1`.
* **Slop:** The number of position moves or edits allowed between terms. `slop: 1` allows 1 intervening word.

## Mental model
```text
Doc 1: "Distributed [0] Systems [1]" ──► Adjacent (diff = 1) ──► Match Phrase (slop=0)
Doc 2: "Distributed [0] Database [1] Systems [2]" ──► Intervening word ──► Match Phrase (slop=1)
```

## Build it
See `code/positional_index.py` building a positional index and phrase matcher in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/17-phrase-search/experiments/run_experiment.sh
```

## Inspect it
Test `match_phrase` with varying slop values:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "match_phrase": {
      "title": { "query": "ergonomic chair", "slop": 0 }
    }
  }
}'
```

## Measure it
Compare phrase query execution time against a standard boolean `match` query: phrase search is slower because it must intersect token positions, not just document IDs.

## Break it
Increase slop to 100 on a long document corpus and observe query latency rise due to wide positional window checks.

## Recover it
Keep slop low (0 to 2) for strict phrase matching.

## Modify it
Use `match_phrase_prefix` for autocomplete search.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does storing term positions increase the size of an inverted index on disk?
2. What does a `slop` of 2 permit between two query terms?

## Guarantees
* `match_phrase` guarantees that terms appear in the specified relative order within the slop window.

## Non-guarantees
* Phrase queries do not evaluate semantic similarity beyond token order.

## When to use this
* Exact titles, quotes, technical idioms, and address matching.

## When not to use this
* Broad exploratory queries where word order is irrelevant.

## What comes next
In Phase 18, we investigate Prefix, Wildcard, and Regex queries.
""",
"""#!/usr/bin/env python3
from collections import defaultdict

class PositionalIndex:
    def __init__(self):
        # term -> doc_id -> list of positions
        self.index = defaultdict(lambda: defaultdict(list))
        self.docs = {}

    def add_doc(self, doc_id, text):
        self.docs[doc_id] = text
        words = text.lower().split()
        for pos, word in enumerate(words):
            self.index[word][doc_id].append(pos)

    def match_phrase(self, phrase, slop=0):
        words = phrase.lower().split()
        if not words:
            return []
        first_term = words[0]
        candidate_docs = set(self.index[first_term].keys())
        for w in words[1:]:
            candidate_docs.intersection_update(self.index[w].keys())

        matches = []
        for doc_id in candidate_docs:
            if self._check_positions(doc_id, words, slop):
                matches.append(doc_id)
        return matches

    def _check_positions(self, doc_id, words, slop):
        pos_lists = [self.index[w][doc_id] for w in words]
        for p0 in pos_lists[0]:
            current = p0
            matched = True
            for next_list in pos_lists[1:]:
                valid = [p for p in next_list if 0 < (p - current) <= (1 + slop)]
                if not valid:
                    matched = False
                    break
                current = valid[0]
            if matched:
                return True
        return False

if __name__ == "__main__":
    idx = PositionalIndex()
    idx.add_doc(1, "distributed systems architecture in cloud")
    idx.add_doc(2, "distributed database storage systems design")
    idx.add_doc(3, "operating systems distributed across machines")

    print("Phrase: 'distributed systems' (slop=0) -> Docs:", idx.match_phrase("distributed systems", slop=0))
    print("Phrase: 'distributed systems' (slop=2) -> Docs:", idx.match_phrase("distributed systems", slop=2))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 17: Positional Index & Phrase Search ==="
python3 phases/17-phrase-search/code/17_phrase_search.py
"""),

        (18, "Prefix, Wildcard, Regex",
         "Leading wildcards turn O(log M) index lookups into full dictionary scans.",
         """# Lesson 18.1: Prefix, Wildcard, Regex

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
""",
"""#!/usr/bin/env python3
import time
import bisect
import re

def build_sorted_terms(count=50000):
    terms = [f"item_{i:06d}_suffix" for i in range(count)]
    terms.append("elasticsearch_engine")
    terms.append("elastic_cloud")
    terms.sort()
    return terms

def prefix_search(terms, prefix):
    # O(log N) prefix scan
    start = bisect.bisect_left(terms, prefix)
    hits = []
    while start < len(terms) and terms[start].startswith(prefix):
        hits.append(terms[start])
        start += 1
    return hits

def regex_scan(terms, pattern_str):
    # O(N) full dictionary iteration
    rx = re.compile(pattern_str)
    return [t for t in terms if rx.search(t)]

if __name__ == "__main__":
    terms = build_sorted_terms(100000)
    
    t0 = time.perf_counter()
    p_hits = prefix_search(terms, "elastic")
    p_time = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    r_hits = regex_scan(terms, r".*search.*")
    r_time = (time.perf_counter() - t0) * 1000

    print(f"Prefix search 'elastic*':    {p_time:.4f} ms (Hits: {len(p_hits)})")
    print(f"Regex scan '.*search.*':     {r_time:.4f} ms (Hits: {len(r_hits)})")
    print(f"Prefix search was {r_time / p_time:.1f}x faster!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 18: Prefix vs Wildcard Benchmark ==="
python3 phases/18-prefix,-wildcard,-regex/code/18_prefix_wildcard.py
"""),

        (19, "Fuzzy Search",
         "Fuzziness is typo tolerance via Damerau-Levenshtein edit distance, NOT semantic similarity.",
         """# Lesson 19.1: Fuzzy Search

## Motto
"Fuzziness is typo tolerance via Damerau-Levenshtein edit distance, NOT semantic similarity."

## Problem
Users misspell words frequently: `"elastcisearch"`, `"phne"`, `"macbok"`. If a search engine only performs exact term lookup, any typo results in zero hits and lost conversions.

## Prediction
Will a fuzzy query with `fuzziness: 1` match `"phone"` when the user types `"phne"`? What if the user types `"fone"`?

## Why this matters
Fuzzy matching recovers from human typing mistakes. However, beginners confuse character edit distance with conceptual similarity.

## First principles
Fuzzy matching calculates the **Damerau-Levenshtein Distance**: the minimum number of single-character operations required to transform word $A$ into word $B$:
1. Insertion (`cst` -> `cost`)
2. Deletion (`coost` -> `cost`)
3. Substitution (`cast` -> `cost`)
4. Transposition of adjacent characters (`csot` -> `cost`)
In Elasticsearch, `fuzziness: "AUTO"` chooses distance based on word length:
* 0..2 chars: edit distance 0 (exact match)
* 3..5 chars: edit distance 1
* > 5 chars: edit distance 2

## Mental model
```text
Query: "elastcisearch" (Length 14)
            │
  [ Transposition: 'ci' -> 'ic' (1 edit) ]
            │
            ▼
Index Term: "elasticsearch" ──► Match! (Distance = 1 <= AUTO limit 2)
```

## Build it
See `code/levenshtein_demo.py` implementing Levenshtein edit distance in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/19-fuzzy-search/experiments/run_experiment.sh
```

## Inspect it
Test fuzzy matching on misspelled query:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "fuzzy": {
      "title": { "value": "ergnomic", "fuzziness": "AUTO" }
    }
  }
}'
```

## Measure it
Notice query latency: expanding fuzzy terms builds a Levenshtein automaton over the term dictionary, which is slightly more expensive than exact term lookup.

## Break it
Set `fuzziness: 2` on short 3-letter words like `"cat"`. Observe false positive noise: `"cat"` matches `"car"`, `"cab"`, `"can"`, `"cap"`, `"hat"`, `"bat"`, `"rat"`.

## Recover it
Use `prefix_length: 2` (requiring the first 2 characters to match exactly before applying edits) and `fuzziness: "AUTO"`.

## Modify it
Combine fuzzy matching with `match` query: `match: { title: { query: "ergnomic chair", fuzziness: "AUTO" } }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `prefix_length` dramatically improve fuzzy query performance?
2. What is the fundamental difference between fuzzy edit distance and semantic vector search?

## Guarantees
* Fuzzy matching guarantees detection of orthographic typos within the specified edit distance.

## Non-guarantees
* Fuzzy matching cannot match phonetic variations (`phonics` vs `fonix`) or semantic synonyms (`car` vs `automobile`).

## When to use this
* User-facing search bars with keyboard input and typo risks.

## When not to use this
* Exact identifiers, serial numbers, IP addresses, or database keys.

## What comes next
In Phase 20, we learn how to expand query recall using Synonyms.
""",
"""#!/usr/bin/env python3

def damerau_levenshtein(s1, s2):
    d = {}
    len1, len2 = len(s1), len(s2)
    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len1):
        for j in range(len2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,       # deletion
                d[(i, j - 1)] + 1,       # insertion
                d[(i - 1, j - 1)] + cost  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + 1) # transposition
    return d[(len1 - 1, len2 - 1)]

if __name__ == "__main__":
    pairs = [
        ("elasticsearch", "elastcisearch"),
        ("phone", "phne"),
        ("keyboard", "keybord"),
        ("cat", "dog")
    ]
    print("Damerau-Levenshtein Edit Distances:")
    for a, b in pairs:
        dist = damerau_levenshtein(a, b)
        print(f"  '{a}' vs '{b}': distance = {dist}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 19: Fuzzy Search & Edit Distance ==="
python3 phases/19-fuzzy-search/code/19_fuzzy_search.py
"""),

        (20, "Synonyms",
         "A search engine must know that laptops are notebooks, but synonyms at index-time cannot be changed without reindexing.",
         """# Lesson 20.1: Synonyms

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
""",
"""#!/usr/bin/env python3

class SynonymExpander:
    def __init__(self, rules):
        self.synonyms = {}
        for rule in rules:
            words = [w.strip().lower() for w in rule.split(",")]
            for w in words:
                self.synonyms[w] = words

    def expand_query(self, query):
        tokens = query.lower().split()
        expanded = []
        for t in tokens:
            if t in self.synonyms:
                expanded.append(f"({' OR '.join(self.synonyms[t])})")
            else:
                expanded.append(t)
        return " AND ".join(expanded)

if __name__ == "__main__":
    rules = [
        "laptop, notebook, portable computer",
        "wireless, cordless",
        "screen, monitor, display"
    ]
    exp = SynonymExpander(rules)
    user_query = "wireless laptop screen"
    print("User Query:     ", user_query)
    print("Expanded Query: ", exp.expand_query(user_query))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 20: Synonym Graph Filter ==="
python3 phases/20-synonyms/code/20_synonyms.py
"""),

        (21, "Autocomplete",
         "Autocomplete requires sub-10ms response: compare prefix queries, edge n-grams, and completion suggesters.",
         """# Lesson 21.1: Autocomplete

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
""",
"""#!/usr/bin/env python3
from collections import defaultdict
import time

class EdgeNGramIndex:
    def __init__(self, min_gram=2, max_gram=5):
        self.min_gram = min_gram
        self.max_gram = max_gram
        self.index = defaultdict(list)

    def add(self, doc_id, text):
        for word in text.lower().split():
            length = len(word)
            for g in range(self.min_gram, min(self.max_gram + 1, length + 1)):
                gram = word[:g]
                self.index[gram].append((doc_id, text))

    def suggest(self, prefix):
        return self.index.get(prefix.lower(), [])

if __name__ == "__main__":
    catalog = EdgeNGramIndex()
    items = ["mechanical keyboard", "ergonomic mouse", "membrane switch", "monitor stand"]
    for i, it in enumerate(items):
        catalog.add(i, it)

    print("Index Terms generated for Edge N-Grams:")
    for k in sorted(catalog.index.keys()):
        print(f"  '{k}' -> {[it for _, it in catalog.index[k]]}")

    prefix = "mech"
    print(f"\\nQuerying prefix '{prefix}':")
    print(catalog.suggest(prefix))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 21: Autocomplete Architectures ==="
python3 phases/21-autocomplete/code/21_autocomplete.py
"""),

        (22, "N-grams",
         "N-grams trade disk storage for lookup velocity: generate substrings at index time to avoid wildcards at query time.",
         """# Lesson 22.1: N-grams

## Motto
"N-grams trade disk storage for lookup velocity: generate substrings at index time to avoid wildcards at query time."

## Problem
Searching inside words (substring matching, e.g. finding `"1234"` inside serial number `"AB-1234-XYZ"`) requires expensive regex scans unless substrings are pre-indexed.

## Prediction
If you generate 3-grams to 5-grams for every word in a document, by what multiple will the number of indexed terms increase?

## Why this matters
N-grams are essential for non-spaced languages (Chinese, Japanese), partial SKU matching, and fuzzy autocomplete. But careless n-gram configurations can explode index disk size by $5\times$ to $20\times$.

## First principles
An **n-gram** is a contiguous sequence of $n$ characters:
* Word: `"elastic"`
* 3-grams: `["ela", "las", "ast", "sti", "tic"]`
* **Edge n-grams:** Only sequences anchored to the start of the word:
  `["el", "ela", "elas", "elast", "elasti", "elastic"]`

## Mental model
```text
Standard Token:  "search" ──► 1 term in index
3-to-4 N-grams:  "search" ──► ["sea", "sear", "ear", "earc", "arc", "arch", "rch"] (7 terms!)
                              Disk space expands significantly!
```

## Build it
See `code/ngram_generator.py` measuring term multiplication factor across sample texts.

## Use Elasticsearch
Run the experiment:
```bash
./phases/22-n-grams/experiments/run_experiment.sh
```

## Inspect it
Use `_analyze` with an `ngram` token filter:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": [
    { "type": "ngram", "min_gram": 3, "max_gram": 4 }
  ],
  "text": "elastic"
}'
```

## Measure it
Measure index disk size before and after adding n-gram analysis.

## Break it
Configure `min_gram: 1` and `max_gram: 10` on large text bodies and observe disk storage and indexing latency skyrocket.

## Recover it
Constrain n-grams: use `edge_ngram` anchored to word boundaries with `min_gram: 2` and `max_gram: 8`.

## Modify it
Compare `ngram` vs `edge_ngram` for search-as-you-type.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an edge n-gram produce fewer terms than a standard n-gram?
2. When should n-gram filters be applied at index time versus search time?

## Guarantees
* Pre-indexing n-grams converts substring searches into instant exact term lookups.

## Non-guarantees
* N-grams do not prevent disk bloat if grammar bounds are set too wide.

## When to use this
* Partial serial numbers, code fragments, and language-independent substring search.

## When not to use this
* Large body paragraphs or general natural language articles.

## What comes next
In Phase 23, we synthesize these tools into a complete Search-As-You-Type design.
""",
"""#!/usr/bin/env python3

def generate_ngrams(word, min_n=3, max_n=5):
    ngrams = []
    L = len(word)
    for n in range(min_n, max_n + 1):
        for i in range(L - n + 1):
            ngrams.append(word[i:i+n])
    return ngrams

def generate_edge_ngrams(word, min_n=2, max_n=6):
    return [word[:n] for n in range(min_n, min(max_n + 1, len(word) + 1))]

if __name__ == "__main__":
    word = "elasticsearch"
    ng = generate_ngrams(word, 3, 4)
    eng = generate_edge_ngrams(word, 2, 6)
    print(f"Original word: '{word}' (1 term)")
    print(f"Standard N-grams (3-4): {len(ng)} terms -> {ng}")
    print(f"Edge N-grams (2-6):     {len(eng)} terms -> {eng}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 22: N-grams & Index Expansion ==="
python3 phases/22-n-grams/code/22_n_grams.py
"""),

        (23, "Search-As-You-Type Design",
         "A great search-as-you-type experience balances prefix matching, ranking popularity, and typo resilience.",
         """# Lesson 23.1: Search-As-You-Type Design

## Motto
"A great search-as-you-type experience balances prefix matching, ranking popularity, and typo resilience."

## Problem
Building a responsive search bar requires handling unfinished words (`wirel`), partial terms (`keyb`), and occasional typos simultaneously, while ranking popular items higher than obscure matches.

## Prediction
What mapping configuration allows matching prefixes on the last entered token while applying BM25 scoring and popularity boosts?

## Why this matters
Elasticsearch provides the dedicated `search_as_you_type` field type (introduced in 7.x and mature in 8.x) that automatically creates root, 2-gram, and 3-gram shingle subfields.

## First principles
The `search_as_you_type` field type generates:
* `field`: standard analyzed text
* `field._2gram`: 2-word shingles with edge n-grams
* `field._3gram`: 3-word shingles with edge n-grams
* `field._index_prefix`: edge n-grams on the last term

## Mental model
```text
User Types: "wireless mech"
                  │
   [ Multi-Match bool query ]
      ├── Match on root text
      └── Prefix match on _index_prefix / _2gram
                  │
                  ▼
Result: "Wireless Mechanical Gaming Keyboard" (Instant Hit)
```

## Build it
See `code/search_as_you_type_sim.py` demonstrating query rewriting for prefix and popularity weighting.

## Use Elasticsearch
Run the experiment:
```bash
./phases/23-search-as-you-type-design/experiments/run_experiment.sh
```

## Inspect it
Create an index with `search_as_you_type` and inspect its generated subfields:
```bash
curl -X PUT http://localhost:9200/sayt_demo -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "name": { "type": "search_as_you_type" }
    }
  }
}'
```

## Measure it
Measure query latency as query length increases from 1 to 10 characters.

## Break it
Use `search_as_you_type` on large article body fields instead of short title/name fields.

## Recover it
Restrict `search_as_you_type` to short titles, product names, and navigation entities.

## Modify it
Add function score or field value factor (`boost: popularity`) to sort suggestions by customer purchase volume.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `search_as_you_type` automatically create 2-gram and 3-gram subfields?
2. How does `bool` query structure ensure complete words are scored higher than partial prefixes?

## Guarantees
* Provides sub-15ms prefix search without managing custom analyzer chains manually.

## Non-guarantees
* Consumes more disk space than standard `text` fields due to automatic shingle subfields.

## When to use this
* E-commerce, SaaS, and document catalog search bars.

## When not to use this
* Massive unstructured text bodies.

## What comes next
In Phase 24, we shift from textual analysis to Numeric and Date Fields (BKD Trees).
""",
"""#!/usr/bin/env python3

class SearchAsYouTypeSim:
    def __init__(self, catalog):
        self.catalog = catalog

    def query(self, prefix_input):
        terms = prefix_input.lower().split()
        if not terms:
            return []
        complete_terms = terms[:-1]
        last_prefix = terms[-1]

        hits = []
        for item in self.catalog:
            title_lower = item["title"].lower()
            # Must match all complete terms
            if complete_terms and not all(ct in title_lower for ct in complete_terms):
                continue
            # Must match prefix on last term
            words = title_lower.split()
            if any(w.startswith(last_prefix) for w in words):
                # Score = popularity + bonus for exact word match
                score = item["popularity"]
                if any(w == last_prefix for w in words):
                    score += 50
                hits.append((item["title"], score))

        hits.sort(key=lambda x: x[1], reverse=True)
        return hits

if __name__ == "__main__":
    products = [
        {"title": "Wireless Mechanical Keyboard", "popularity": 1200},
        {"title": "Wireless Mouse", "popularity": 2500},
        {"title": "Wired Gaming Keyboard", "popularity": 800},
        {"title": "Wireless Ergonomic Trackball", "popularity": 300}
    ]
    engine = SearchAsYouTypeSim(products)
    print("User types 'wirel':")
    for title, s in engine.query("wirel"):
        print(f"  - {title} (score: {s})")
    print("\\nUser types 'wirel mech':")
    for title, s in engine.query("wirel mech"):
        print(f"  - {title} (score: {s})")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 23: Search-As-You-Type Simulation ==="
python3 phases/23-search-as-you-type-design/code/23_search_as_you_type_design.py
"""),

        (24, "Numeric and Date Fields",
         "Numbers and dates do not belong in inverted indexes: BKD trees provide O(log N) multi-dimensional range queries.",
         """# Lesson 24.1: Numeric and Date Fields

## Motto
"Numbers and dates do not belong in inverted indexes: BKD trees provide O(log N) multi-dimensional range queries."

## Problem
Inverted indexes excel at finding exact terms (`"status: active"`). But for range queries (`price BETWEEN 50 AND 100` or `date >= 2026-01-01`), an inverted index must evaluate every single discrete number in the range, creating thousands of boolean clauses!

## Prediction
How does Lucene physically organize numbers on disk to make range queries fast?

## Why this matters
Elasticsearch uses **BKD Trees** (Block K-d Trees, point fields: `integer`, `long`, `float`, `double`, `date`) for numeric range queries.

## First principles
A **BKD Tree** is a space-partitioning binary tree that recursively divides multidimensional coordinate spaces:
* Leaf nodes store compact blocks of numeric points.
* A range query tests the bounding box of the tree node:
  * Node completely inside range $\to$ add all documents in leaf instantly.
  * Node completely outside range $\to$ skip entire branch.
  * Node intersects range boundary $\to$ recurse down children.

## Mental model
```text
                     [0 to 1000]
                    /           \
             [0 to 500]       [501 to 1000]
             /        \
         [0 to 250]  [251 to 500]
Range Query: price >= 600
  ──► Skips left half [0 to 500] in O(1) time!
```

## Build it
See `code/bkd_tree_sim.py` demonstrating recursive 1D range partitioning in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/24-numeric-and-date-fields/experiments/run_experiment.sh
```

## Inspect it
Create an index with numeric and date fields and issue a range query:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "range": {
      "price": { "gte": 50, "lte": 200 }
    }
  }
}'
```

## Measure it
Compare range query speed on a numeric field vs an un-indexed text string.

## Break it
Store a price as a string (`"price": "149.99"`) and run a string range query: `"149.99"` comes before `"50.00"` lexicographically!

## Recover it
Map the field as `double` or `scaled_float`.

## Modify it
Use date math syntax: `"gte": "now-7d/d"`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are BKD trees superior to inverted indexes for continuous range queries?
2. What is `scaled_float` and when is it preferred over `double`?

## Guarantees
* Point fields provide logarithmic time range evaluations.

## Non-guarantees
* Continuous point fields do not support standard text tokenization or stemming.

## When to use this
* Prices, timestamps, latency metrics, counts, and geographic coordinates.

## When not to use this
* Categorical IDs that are only queried for exact equality (use `keyword` instead).

## What comes next
In Phase 25, we explore Geo Search (points, bounding boxes, and distance calculations).
""",
"""#!/usr/bin/env python3

class Simple1DPointIndex:
    def __init__(self, data):
        # data: list of (doc_id, value)
        self.sorted_data = sorted(data, key=lambda x: x[1])

    def range_query(self, min_val, max_val):
        # Binary search boundaries
        import bisect
        keys = [v for _, v in self.sorted_data]
        left = bisect.bisect_left(keys, min_val)
        right = bisect.bisect_right(keys, max_val)
        return [self.sorted_data[i][0] for i in range(left, right)]

if __name__ == "__main__":
    prices = [(1, 19.99), (2, 49.99), (3, 89.99), (4, 129.99), (5, 299.99)]
    index = Simple1DPointIndex(prices)
    min_p, max_p = 40.0, 150.0
    matching_ids = index.range_query(min_p, max_p)
    print(f"Prices: {prices}")
    print(f"Query range [{min_p}, {max_p}] -> Matching Doc IDs: {matching_ids}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 24: Numeric and Date Fields ==="
python3 phases/24-numeric-and-date-fields/code/24_numeric_and_date_fields.py
"""),

        (25, "Geo Search",
         "Earth is a sphere, not a flat plane: geo search uses spatial BKD trees and Haversine distance.",
         """# Lesson 25.1: Geo Search

## Motto
"Earth is a sphere, not a flat plane: geo search uses spatial BKD trees and Haversine distance."

## Problem
In mobile delivery apps and local store finders, users search for: *"coffee shops within 2 kilometers of my current latitude and longitude"*. Naive SQL bounding boxes do not account for Earth's curvature or circular radii.

## Prediction
Will a rectangular bounding box query return stores that are in the corners of the box but farther than 2 km from the center?

## Why this matters
Elasticsearch indexes `geo_point` fields using 2-dimensional BKD trees (spatial points) for spatial bounding boxes and radial distance filters.

## First principles
* **`geo_point`:** Latitude and Longitude pair: `{"lat": 40.7128, "lon": -74.0060}`.
* **Haversine Formula:** Calculates great-circle distance between two points on a sphere of radius $R$:
  $$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$

## Mental model
```text
      ┌─────────────────────────┐
      │   Corner (Distance > R) │
      │      ┌───────────┐      │
      │      │  RADIUS   │      │
      │      │    (R)    │      │
      │      └───────────┘      │
      │  Bounding Box Rectangle │
      └─────────────────────────┘
  Geo-Distance enforces circular radius; Bounding Box is faster rectangular filter.
```

## Build it
See `code/haversine_distance.py` calculating spatial distances and radial filters in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/25-geo-search/experiments/run_experiment.sh
```

## Inspect it
Create an index with `geo_point` mapping and execute a `geo_distance` query:
```bash
curl -X POST http://localhost:9200/stores/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "filter": {
        "geo_distance": {
          "distance": "5km",
          "location": { "lat": 37.7749, "lon": -122.4194 }
        }
      }
    }
  }
}'
```

## Measure it
Measure query latency comparing `geo_bounding_box` (simple coordinate checks) vs `geo_distance` (trigonometric calculations).

## Break it
Swap latitude and longitude values: latitude must be between $-90$ and $+90$; longitude between $-180$ and $+180$. Elasticsearch rejects invalid ranges with `illegal_argument_exception`.

## Recover it
Follow the GeoJSON standard: `[lon, lat]` in arrays, or explicit `{"lat": ..., "lon": ...}` in objects.

## Modify it
Sort results by distance from user location: `sort: [{ "_geo_distance": { "location": ... } }]`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `geo_bounding_box` execute faster than `geo_distance`?
2. What coordinate order does Elasticsearch expect when geo points are provided as an array?

## Guarantees
* Provides accurate spherical distance calculations across the globe.

## Non-guarantees
* Does not compute street navigation routing distance or traffic conditions.

## When to use this
* Store locators, ride sharing, delivery radius, and spatial analytics.

## When not to use this
* Complex multi-polygon GIS spatial topology operations (use PostGIS for complex GIS).

## What comes next
In Phase 26, we begin the next major milestone: Aggregations and Analytics From First Principles.
""",
"""#!/usr/bin/env python3
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    # San Francisco coords
    user_lat, user_lon = 37.7749, -122.4194
    stores = [
        {"name": "Downtown SF Store", "lat": 37.7833, "lon": -122.4167},
        {"name": "Oakland Store", "lat": 37.8044, "lon": -122.2712},
        {"name": "San Jose Store", "lat": 37.3382, "lon": -121.8863}
    ]
    print(f"User location: ({user_lat}, {user_lon})\\n")
    for s in stores:
        dist = haversine(user_lat, user_lon, s["lat"], s["lon"])
        within_15km = dist <= 15.0
        print(f"Store: {s['name']:20s} | Distance: {dist:6.2f} km | Within 15km: {within_15km}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 25: Geo Search & Haversine Distance ==="
python3 phases/25-geo-search/code/25_geo_search.py
""")
    ]

    for p_num, p_title, motto, doc_content, code_content, exp_content in phases:
        slug = f"{p_num:02d}-{p_title.lower().replace(' ', '-').replace('/', '-')}"
        phase_dir = os.path.join(PHASES_DIR, slug)
        write_file(os.path.join(phase_dir, "docs", "en.md"), doc_content)
        write_file(os.path.join(phase_dir, "code", f"{slug.replace('-', '_')}.py"), code_content)
        write_file(os.path.join(phase_dir, "experiments", "run_experiment.sh"), exp_content)
        write_file(os.path.join(phase_dir, "outputs", "evidence-template.md"), evidence_template(p_title, p_num))
        print(f"Generated Phase {p_num:02d}: {p_title}")

if __name__ == "__main__":
    generate_phases_11_to_25()
