#!/usr/bin/env python3
"""
build_curriculum_part1.py - Generates Phases 00 to 25 for elasticsearch-from-scratch.
Adheres strictly to LESSON_TEMPLATE.md and pedagogical guidelines.
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

## Index Settings & Mappings
```json
{{}}
```

## Query or Payload
```json
{{}}
```

## Important Terminal Output
```text
```

## Measurements
* Metric 1:
* Metric 2:
* Metric 3:

## What Actually Happened?
Describe the observed behavior vs your initial prediction:

## What Surprised Me?

## What Did I Intentionally Break?

## How Did I Diagnose It?

## How Did I Recover?

## What Did I Modify?

## Artifact Produced:

## Explain the Concept in My Own Words:

## Guarantees:

## Non-guarantees:

## When to Use This:

## When NOT to Use This:

## Remaining Questions:
"""

def generate_phases_00_to_25():
    phases = [
        (0, "Environment and Search Lab",
         "A search engine is not magic; it is an HTTP daemon listening on a TCP socket, parsing JSON, and writing to Lucene segments.",
         "Single-node Elasticsearch REST environment setup and API health inspection.",
         """# Lesson 00.1: Environment and Search Lab

## Motto
"A search engine is not magic; it is an HTTP daemon listening on a TCP socket, parsing JSON, and writing to Lucene segments."

## Problem
Developers often treat Elasticsearch as a complex black-box service. Without understanding its runtime boundaries (JVM heap, TCP ports 9200 and 9300, and HTTP REST interface), diagnosing connection drops or cluster health issues is impossible.

## Prediction
Will Elasticsearch respond to a standard HTTP GET request on port 9200 using a generic `curl` command, without any proprietary client SDK?

## Why this matters
Elasticsearch is fundamentally an HTTP/REST engine. Every action—indexing, searching, checking health, re-routing shards—is an HTTP verb (`GET`, `POST`, `PUT`, `DELETE`) with a JSON payload.

## First principles
Elasticsearch binds to two network ports:
1. **Port 9200 (HTTP REST):** Client communication, queries, indexing, and cluster management.
2. **Port 9300 (Transport/TCP):** Internal node-to-node cluster communication, shard replication, and cluster state broadcasting.

## Mental model
```text
Client (curl / python requests)
          │
          │ HTTP JSON (port 9200)
          ▼
┌───────────────────────────────────────────────┐
│              Elasticsearch Node               │
│ - Netty HTTP Transport Engine                 │
│ - REST Handlers (/ _search, /_cluster, /_cat) │
│ - JVM Runtime (Heap & GC)                     │
│ - Apache Lucene Index Store                   │
└───────────────────────────────────────────────┘
```

## Build it
See `code/check_node.py` which connects to Elasticsearch using raw Python `urllib` without third-party dependencies.

## Use Elasticsearch
```bash
./phases/00-environment-and-search-lab/experiments/run_experiment.sh
```

## Inspect it
```bash
curl -s http://localhost:9200/
curl -s http://localhost:9200/_cluster/health?pretty
```

## Measure it
Measure response latency of the root ping endpoint:
```bash
curl -o /dev/null -s -w 'Total time: %{time_total}s\\n' http://localhost:9200/
```

## Break it
Kill the Elasticsearch container or block port 9200, and observe how client connections fail with `ConnectionRefusedError`.

## Recover it
Restart the container via `make up` and observe cluster recovery.

## Modify it
Change the container memory limit in `docker-compose.yml` (`ES_JAVA_OPTS=-Xms256m -Xmx256m`) and verify JVM heap in `_nodes/stats/jvm`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch use two separate network ports (9200 vs 9300)?
2. What happens to HTTP requests if the JVM is undergoing a Stop-The-World garbage collection pause?

## Guarantees
* Elasticsearch provides a standard HTTP/1.1 REST interface for all operations.

## Non-guarantees
* Elasticsearch does not guarantee ACID multi-document transactions across shards.

## When to use this
* As the foundation for every search, indexing, and administrative task in the course.

## When not to use this
* Never expose port 9200 directly to the public internet without authentication and TLS.

## What comes next
In Phase 01, we will explore why relational database table scans fail at full-text search, necessitating inverted indexes.
""",
"""#!/usr/bin/env python3
import json
import urllib.request
import sys

def check_es(url="http://localhost:9200"):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("Successfully connected to Elasticsearch!")
            print(f"Cluster Name: {data.get('cluster_name')}")
            print(f"Node Name:    {data.get('name')}")
            print(f"ES Version:   {data.get('version', {}).get('number')}")
            print(f"Lucene Ver:   {data.get('version', {}).get('lucene_version')}")
            return True
    except Exception as e:
        print(f"Failed to connect to {url}: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = check_es()
    sys.exit(0 if success else 1)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 00 Experiment: Verifying Elasticsearch Lab ==="
python3 phases/00-environment-and-search-lab/code/check_node.py
curl -s http://localhost:9200/_cluster/health | grep -q "status" && echo "Cluster health check passed!"
"""),

        (1, "Why Search Engines Exist",
         "Linear scan is O(N) in text length and document count; search engines invert the problem to O(1) term lookup.",
         "Demonstrate why brute-force text search fails as dataset size grows.",
         """# Lesson 01.1: Why Search Engines Exist

## Motto
"Linear scan is O(N) in text length and document count; search engines invert the problem to O(1) term lookup."

## Problem
When searching unstructured text inside a relational database using `WHERE description LIKE '%wireless%'`, the database must read every single record and perform a substring scan. As the dataset grows to millions of rows, search latency spikes from milliseconds to tens of seconds.

## Prediction
How much does search latency increase when linearly scanning 10,000 product descriptions versus 1,000 product descriptions for a specific keyword?

## Why this matters
Traditional B-Tree indexes only index column prefixes (e.g. `LIKE 'wireless%'`). They cannot index arbitrary interior words without scanning the entire table.

## First principles
Scanning $N$ documents each containing $L$ characters takes $O(N \times L)$ comparisons. In contrast, an inverted index maps words to document IDs in advance, making search proportional to the number of matching documents, not total corpus size.

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
""",
"""#!/usr/bin/env python3
import time

def generate_docs(count):
    terms = ["wireless", "mechanical", "ergonomic", "bluetooth", "gaming", "portable", "battery", "fast", "quiet"]
    docs = []
    for i in range(count):
        desc = f"Product {i} has high quality features: {terms[i % len(terms)]} design with durable components."
        docs.append({"id": i, "description": desc})
    return docs

def linear_search(docs, term):
    hits = []
    for doc in docs:
        if term in doc["description"]:
            hits.append(doc["id"])
    return hits

if __name__ == "__main__":
    for size in [1000, 10000, 50000]:
        corpus = generate_docs(size)
        start = time.perf_counter()
        hits = linear_search(corpus, "wireless")
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Corpus size: {size:6d} docs | Hits: {len(hits):5d} | Latency: {elapsed:.3f} ms")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 01: Benchmarking Linear Document Scan ==="
python3 phases/01-why-search-engines-exist/code/linear_vs_index.py
"""),

        (2, "Build an Inverted Index",
         "The inverted index is the atom of search: map terms to sorted document IDs, and search becomes set intersection.",
         "Construct a pure Python inverted index and compare its lookup speed with linear scan.",
         """# Lesson 02.1: Build an Inverted Index

## Motto
"The inverted index is the atom of search: map terms to sorted document IDs, and search becomes set intersection."

## Problem
In Phase 01, linear scan required checking every document. We need an indexing data structure where looking up any word immediately gives us the exact list of matching documents in $O(1)$ time.

## Prediction
Will building an in-memory inverted index permit query execution in under 0.05 milliseconds regardless of corpus size?

## Why this matters
Every modern search engine (Elasticsearch, Lucene, Solr, Tantivy) is fundamentally an inverted index manager. Mastering this structure removes all mysticism from full-text search.

## First principles
A forward index maps:
`Document ID -> [List of Words]`
An **inverted index** inverts this relationship:
`Word (Term) -> [Sorted List of Document IDs]` (called the Postings List).

## Mental model
```text
Documents:
  Doc 1: "redis cache"
  Doc 2: "kafka log stream"
  Doc 3: "redis stream"

Inverted Index:
  cache  ──► [1]
  kafka  ──► [2]
  log    ──► [2]
  redis  ──► [1, 3]
  stream ──► [2, 3]
```

## Build it
See `code/mini_search.py` which builds a dictionary-based inverted index supporting `index()` and `search()`.

## Use Elasticsearch
Run the experiment:
```bash
./phases/02-build-an-inverted-index/experiments/run_experiment.sh
```

## Inspect it
Inspect the postings list generated for common terms in `code/mini_search.py`.

## Measure it
Compare query latency: linear scan ($O(N)$) vs inverted index ($O(1)$ dictionary lookup).

## Break it
Search for uppercase `"Redis"` in our naive inverted index without normalization. Observe that it fails to match `"redis"`.

## Recover it
This limitation motivates Phase 03 (Tokenization) and Phase 04 (Normalization).

## Modify it
Extend `mini_search.py` to index 20,000 documents and measure index construction time vs query time.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must the postings list be stored in sorted order by Document ID?
2. What is the space-time trade-off of maintaining an inverted index?

## Guarantees
* Query time is independent of non-matching document volume.

## Non-guarantees
* An inverted index does not preserve document sentence structure or formatting.

## When to use this
* As the foundational data structure for any full-text or tokenized attribute search.

## When not to use this
* When data changes every millisecond and write throughput cannot tolerate index updates.

## What comes next
In Phase 03, we explore tokenization: converting arbitrary strings into discrete index terms.
""",
"""#!/usr/bin/env python3
import time
from collections import defaultdict

class MiniInvertedIndex:
    def __init__(self):
        # term -> sorted list of doc_ids
        self.index = defaultdict(list)
        self.documents = {}

    def add_document(self, doc_id, text):
        self.documents[doc_id] = text
        # Simple whitespace splitting for now
        tokens = text.lower().split()
        seen = set()
        for token in tokens:
            if token not in seen:
                self.index[token].append(doc_id)
                seen.add(token)

    def search(self, term):
        term = term.lower()
        return self.index.get(term, [])

if __name__ == "__main__":
    engine = MiniInvertedIndex()
    docs = [
        "Distributed search with Elasticsearch",
        "Apache Kafka event streaming architecture",
        "Redis in-memory caching and search",
        "Distributed database replication and sharding"
    ]
    for idx, doc in enumerate(docs):
        engine.add_document(idx, doc)

    query = "distributed"
    start = time.perf_counter()
    results = engine.search(query)
    elapsed = (time.perf_counter() - start) * 1000

    print(f"Query: '{query}' -> Matching Doc IDs: {results}")
    print(f"Matching Documents:")
    for doc_id in results:
        print(f"  - [{doc_id}]: {engine.documents[doc_id]}")
    print(f"Lookup Latency: {elapsed:.4f} ms")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 02: Building Inverted Index From Scratch ==="
python3 phases/02-build-an-inverted-index/code/mini_search.py
"""),

        (3, "Tokenization",
         "Before you can index text, you must define what constitutes a word.",
         "Explore token boundaries, punctuation handling, numbers, and hyphens.",
         """# Lesson 03.1: Tokenization

## Motto
"Before you can index text, you must define what constitutes a word."

## Problem
Raw strings like `"Redis, Kafka and Elasticsearch!"` contain punctuation, commas, hyphens, and whitespace. If a naive index simply splits on spaces, the token `"Elasticsearch!"` will never match a query for `"Elasticsearch"`.

## Prediction
What happens if you index `"Wi-Fi 6E"` with a naive whitespace tokenizer versus a punctuation-stripping tokenizer?

## Why this matters
Search quality lives or dies on tokenization. Tokenizing too aggressively splits meaningful domain terms (like `C++` or `e-commerce`), while tokenizing too passively leaves noisy punctuation attached to words.

## First principles
A tokenizer consumes a character stream and produces a token stream, recording:
* The token string (`term`)
* Start and end character offsets in the original text
* Position in the token stream (for phrase queries)

## Mental model
```text
Raw Text: "Distributed, fault-tolerant search!"
                       │
             [ Tokenizer Stage ]
                       │
Emitted Tokens:
 1. "Distributed"  (offset: 0-11,  pos: 0)
 2. "fault"        (offset: 13-18, pos: 1)
 3. "tolerant"     (offset: 19-27, pos: 2)
 4. "search"       (offset: 28-34, pos: 3)
```

## Build it
See `code/tokenizer_experiments.py` demonstrating whitespace, regex word boundary, and punctuation-aware tokenization.

## Use Elasticsearch
Run the experiment using Elasticsearch's `_analyze` API:
```bash
./phases/03-tokenization/experiments/run_experiment.sh
```

## Inspect it
Observe the output of the standard tokenizer:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "text": "Redis, Kafka and Elasticsearch!"
}'
```

## Measure it
Inspect token count and emitted offsets.

## Break it
Send email addresses (`alice@example.com`) or URLs (`https://elastic.co`) through `standard` tokenizer vs `whitespace` tokenizer and observe where standard tokenizer fractures domains.

## Recover it
Choose domain-specific tokenizers (e.g. `uax_url_email`) when indexing structured identifiers.

## Modify it
Configure custom pattern tokenizers with custom regexes.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the standard tokenizer strip punctuation but preserve alphanumeric characters?
2. What information is lost permanently when a tokenizer discards punctuation?

## Guarantees
* Tokenization deterministically maps a character stream to discrete tokens with offsets.

## Non-guarantees
* A single generic tokenizer cannot handle natural language and code identifiers with equal fidelity.

## When to use this
* As the second mandatory stage of any text analysis pipeline.

## When not to use this
* Do not apply full text tokenization to exact identifiers (IDs, SKUs, IP addresses). Use `keyword` mapping instead.

## What comes next
In Phase 04, we introduce token normalization: lowercasing, stop words, and stemming.
""",
"""#!/usr/bin/env python3
import re

def naive_whitespace(text):
    return text.split()

def regex_word_tokenizer(text):
    # Match alphanumeric words, discarding punctuation
    return re.findall(r'\\b\\w+\\b', text)

if __name__ == "__main__":
    sample = "Redis, Kafka, and Elasticsearch 8.17! Email: user@elastic.co, Cost: $49.99"
    print("Input Text:", sample)
    print("\\n1. Naive Whitespace Tokens:")
    print(naive_whitespace(sample))
    print("\\n2. Regex Word Tokens:")
    print(regex_word_tokenizer(sample))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 03: Tokenization Experiments ==="
python3 phases/03-tokenization/code/tokenizer_experiments.py

echo -e "\\n--- Elasticsearch _analyze Standard Tokenizer ---"
curl -s -X POST "http://localhost:9200/_analyze" -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "text": "Redis, Kafka and Elasticsearch 8.17!"
}' | grep -o '"token":"[^"]*"' || echo "Elasticsearch offline."
"""),

        (4, "Normalization",
         "Search must match intent, not typography: casing, accents, and suffixes must be reconciled.",
         "Implement lowercasing, stop-word removal, and algorithmic stemming.",
         """# Lesson 04.1: Normalization

## Motto
"Search must match intent, not typography: casing, accents, and suffixes must be reconciled."

## Problem
A user searching for `"running"` expects to find documents containing `"Run"`, `"running"`, and `"runs"`. Without token normalization, lexical mismatches cause false negatives (zero search results).

## Prediction
Will a search for `"RUNNING"` match a document containing `"Running"` if only lowercasing is applied? What if the document contains `"ran"`?

## Why this matters
Normalization bridges the gap between how authors write content and how users submit queries.

## First principles
Normalization consists of:
1. **Case folding:** Converting uppercase to lowercase (`Running` -> `running`).
2. **Stop word filtering:** Discarding high-frequency, low-information words (`the`, `is`, `at`).
3. **Stemming:** Reducing inflected words to their root stem (`running`, `runs`, `runner` -> `run`).

## Mental model
```text
Tokens: ["Running", "the", "Distributes", "Fast"]
                      │
           [ Lowercase Filter ]
                      │
        ["running", "the", "distributes", "fast"]
                      │
             [ Stop Filter ]
                      │
        ["running", "distributes", "fast"]
                      │
            [ Porter Stemmer ]
                      │
Final:  ["run", "distribut", "fast"]
```

## Build it
See `code/normalizer.py` implementing a miniature normalization pipeline in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/04-normalization/experiments/run_experiment.sh
```

## Inspect it
Test the Porter stemmer via `_analyze`:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": ["lowercase", "stemmer"],
  "text": "Running distributed systems efficiently"
}'
```

## Measure it
Compare token counts and term reduction percentage before and after normalization.

## Break it
Notice stemming over-generalization: `"organization"` and `"organ"` might stem to overlapping roots, causing surprising false positive hits.

## Recover it
Tune stemmer aggressiveness or keep original terms in a multi-field.

## Modify it
Test language-specific stemmers (e.g. `english` vs `german` vs `french`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is stemming not always desirable (e.g. searching for specific legal statutes or chemical formulas)?
2. What is the difference between lemmatization (dictionary-based) and stemming (heuristic rule-based)?

## Guarantees
* Normalization increases search recall (fewer false negatives).

## Non-guarantees
* Normalization does not guarantee 100% precision; aggressive stemming can introduce semantic drift.

## When to use this
* Standard human-readable natural language search fields.

## When not to use this
* Exact codes, UUIDs, SKUs, passwords, and case-sensitive programmatic tokens.

## What comes next
In Phase 05, we assemble Character Filters, Tokenizers, and Token Filters into the full Elasticsearch Analyzer Pipeline.
""",
"""#!/usr/bin/env python3

def lowercase(tokens):
    return [t.lower() for t in tokens]

def remove_stopwords(tokens, stopwords=None):
    if stopwords is None:
        stopwords = {"the", "a", "an", "and", "in", "of", "to", "is", "for"}
    return [t for t in tokens if t not in stopwords]

def naive_suffix_stemmer(tokens):
    stemmed = []
    for t in tokens:
        if t.endswith("ing") and len(t) > 4:
            stemmed.append(t[:-3])
        elif t.endswith("ed") and len(t) > 3:
            stemmed.append(t[:-2])
        elif t.endswith("s") and len(t) > 2 and not t.endswith("ss"):
            stemmed.append(t[:-1])
        else:
            stemmed.append(t)
    return stemmed

if __name__ == "__main__":
    raw_tokens = ["The", "Distributed", "Nodes", "are", "Running", "Fast"]
    print("Raw Tokens:       ", raw_tokens)
    step1 = lowercase(raw_tokens)
    print("1. Lowercased:    ", step1)
    step2 = remove_stopwords(step1)
    print("2. Stop words out:", step2)
    step3 = naive_suffix_stemmer(step2)
    print("3. Stemmed:       ", step3)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 04: Normalization Experiments ==="
python3 phases/04-normalization/code/normalizer.py

echo -e "\\n--- Elasticsearch _analyze with Lowercase & Stemmer ---"
curl -s -X POST "http://localhost:9200/_analyze" -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": ["lowercase", "porter_stem"],
  "text": "The distributed systems are running fast"
}' | grep -o '"token":"[^"]*"' || echo "Elasticsearch offline."
"""),

        (5, "Analyzer Pipeline",
         "An analyzer is a three-stage factory: Character Filters mutate chars, Tokenizer emits tokens, Token Filters refine tokens.",
         "Build and test custom analyzer pipelines using _analyze API.",
         """# Lesson 05.1: Analyzer Pipeline

## Motto
"An analyzer is a three-stage factory: Character Filters mutate chars, Tokenizer emits tokens, Token Filters refine tokens."

## Problem
In production, documents arrive containing dirty HTML markup (`<p>Hello &amp; welcome</p>`), mixed character encodings, and abbreviations. If tokenization occurs before stripping HTML tags, the tags themselves become inverted index terms.

## Prediction
If you process `"<p>Elasticsearch &amp; Lucene</p>"` through a standard analyzer without a character filter, will `p` and `amp` be indexed as terms?

## Why this matters
Understanding the strict 3-stage hierarchy enables designing custom analyzers for e-commerce, legal docs, code repositories, or multilingual catalogs.

## First principles
The analysis pipeline executes strictly in order:
1. **Character Filters (0 or more):** Receive raw characters, emit transformed characters.
2. **Tokenizer (exactly 1):** Receives characters, emits token stream.
3. **Token Filters (0 or more):** Receive tokens, emit modified/filtered tokens.

## Mental model
```text
Raw String: "<b>High-Performance</b> &amp; Fast!"
                    │
   [ Char Filter 1: html_strip ]
                    ▼
            "High-Performance &amp; Fast!"
                    │
   [ Char Filter 2: mapping (&amp; -> and) ]
                    ▼
            "High-Performance and Fast!"
                    │
   [ Tokenizer: standard ]
                    ▼
         ["High", "Performance", "and", "Fast"]
                    │
   [ Token Filter 1: lowercase ]
                    ▼
         ["high", "performance", "and", "fast"]
                    │
   [ Token Filter 2: stop ]
                    ▼
         ["high", "performance", "fast"]
```

## Build it
See `code/custom_analyzer_test.py` simulating the three distinct stages.

## Use Elasticsearch
Run the experiment:
```bash
./phases/05-analyzer-pipeline/experiments/run_experiment.sh
```

## Inspect it
Use the `_analyze` API with inline custom components:
```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "char_filter": ["html_strip"],
  "tokenizer": "standard",
  "filter": ["lowercase", "stop"],
  "text": "<h1>Elasticsearch</h1> is <b>fast</b>!"
}'
```

## Measure it
Inspect token start and end character offsets to see how `html_strip` preserves original character positions for highlighting.

## Break it
Put a token filter before a tokenizer—observe that Elasticsearch rejects the configuration at index creation because the pipeline order is immutable.

## Recover it
Respect the invariant: `char_filter -> tokenizer -> filter`.

## Modify it
Add a synonym filter to the token filter chain.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can an analyzer have multiple character filters and token filters, but only exactly ONE tokenizer?
2. What happens if the query-time analyzer differs from the index-time analyzer?

## Guarantees
* Analysis is deterministic: identical text fed to identical analyzer configs always produces identical terms.

## Non-guarantees
* Analysis cannot reconstruct the original text formatting once terms are emitted.

## When to use this
* Every full-text search field requires a conscious analyzer design.

## When not to use this
* Do not apply analyzers to exact values like UUIDs or IP addresses.

## What comes next
In Phase 06, we move from individual strings to structured JSON documents with heterogeneous fields.
""",
"""#!/usr/bin/env python3
import re
import html

class AnalysisPipeline:
    def __init__(self, char_filters=None, tokenizer=None, token_filters=None):
        self.char_filters = char_filters or []
        self.tokenizer = tokenizer or (lambda text: text.split())
        self.token_filters = token_filters or []

    def analyze(self, text):
        # Stage 1: Char filters
        current_text = text
        for cf in self.char_filters:
            current_text = cf(current_text)
        
        # Stage 2: Tokenizer
        tokens = self.tokenizer(current_text)

        # Stage 3: Token filters
        current_tokens = tokens
        for tf in self.token_filters:
            current_tokens = tf(current_tokens)

        return current_tokens

if __name__ == "__main__":
    def strip_html(t): return re.sub(r'<[^>]+>', '', t)
    def decode_entities(t): return html.unescape(t)
    def word_tokenizer(t): return re.findall(r'\\b\\w+\\b', t)
    def lowercase(tokens): return [t.lower() for t in tokens]
    def remove_stopwords(tokens): return [t for t in tokens if t not in {"is", "and", "the"}]

    pipeline = AnalysisPipeline(
        char_filters=[strip_html, decode_entities],
        tokenizer=word_tokenizer,
        token_filters=[lowercase, remove_stopwords]
    )

    sample = "<h2>Elasticsearch &amp; Lucene</h2> are <b>FAST</b>!"
    terms = pipeline.analyze(sample)
    print("Input: ", sample)
    print("Terms: ", terms)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 05: Analyzer Pipeline Experiments ==="
python3 phases/05-analyzer-pipeline/code/custom_analyzer_test.py

echo -e "\\n--- Elasticsearch _analyze Custom Pipeline ---"
curl -s -X POST "http://localhost:9200/_analyze" -H "Content-Type: application/json" -d '{
  "char_filter": ["html_strip"],
  "tokenizer": "standard",
  "filter": ["lowercase", "stop"],
  "text": "<h2>Elasticsearch &amp; Lucene</h2> are <b>FAST</b>!"
}' | grep -o '"token":"[^"]*"' || echo "Elasticsearch offline."
"""),

        (6, "Documents and Fields",
         "A document is not a blob; it is a dictionary of fields, each demanding its own indexing strategy.",
         "Build per-field indexing in Python and index structured documents into Elasticsearch.",
         """# Lesson 06.1: Documents and Fields

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
""",
"""#!/usr/bin/env python3
from collections import defaultdict

class FieldedMiniIndex:
    def __init__(self):
        self.text_indexes = defaultdict(lambda: defaultdict(list))
        self.exact_indexes = defaultdict(lambda: defaultdict(list))
        self.numeric_store = defaultdict(dict)
        self.docs = {}

    def index_document(self, doc_id, doc):
        self.docs[doc_id] = doc
        for field, value in doc.items():
            if isinstance(value, str):
                # Text tokenized index
                tokens = [t.lower() for t in value.split()]
                for t in set(tokens):
                    self.text_indexes[field][t].append(doc_id)
                # Exact keyword index
                self.exact_indexes[field][value].append(doc_id)
            elif isinstance(value, (int, float)):
                self.numeric_store[field][doc_id] = value

    def search_text(self, field, term):
        return self.text_indexes[field].get(term.lower(), [])

    def filter_range(self, field, min_val, max_val):
        hits = []
        for doc_id, val in self.numeric_store[field].items():
            if min_val <= val <= max_val:
                hits.append(doc_id)
        return hits

if __name__ == "__main__":
    idx = FieldedMiniIndex()
    idx.index_document(1, {"title": "Ergonomic Wireless Keyboard", "category": "electronics", "price": 99.0})
    idx.index_document(2, {"title": "Mechanical Gaming Keyboard", "category": "electronics", "price": 149.0})
    idx.index_document(3, {"title": "Ergonomic Office Chair", "category": "furniture", "price": 299.0})

    print("Search 'title:ergonomic' ->", idx.search_text("title", "ergonomic"))
    print("Filter 'price: 80 to 120' ->", idx.filter_range("price", 80.0, 120.0))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 06: Fielded Document Indexing ==="
python3 phases/06-documents-and-fields/code/fielded_search.py

echo -e "\\n--- Indexing to Elasticsearch ---"
curl -s -X PUT "http://localhost:9200/products_phase06/_doc/1" -H "Content-Type: application/json" -d '{
  "title": "Ergonomic Office Chair",
  "price": 299.99,
  "category": "furniture"
}' || echo "ES offline"

curl -s "http://localhost:9200/products_phase06/_doc/1?pretty" || true
"""),

        (7, "text vs keyword",
         "Text is for searching inside; keyword is for filtering, sorting, and aggregating exactly.",
         "Contrast full-text search with exact matching and implement multi-fields.",
         """# Lesson 07.1: text vs keyword

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
""",
"""#!/usr/bin/env python3

def index_entry(raw_value):
    # text pipeline: lowercase + tokenize
    text_tokens = raw_value.lower().split()
    # keyword pipeline: exact verbatim string
    keyword_token = raw_value
    return {"text_tokens": text_tokens, "keyword_token": keyword_token}

if __name__ == "__main__":
    val = "United States"
    indexed = index_entry(val)
    print("Raw Value:     ", val)
    print("Text Tokens:   ", indexed["text_tokens"])
    print("Keyword Token: ", repr(indexed["keyword_token"]))

    query_term = "United States"
    print(f"\\nQuerying term '{query_term}':")
    print(f"  Matches keyword? {query_term == indexed['keyword_token']}")
    print(f"  Matches in text tokens? {query_term in indexed['text_tokens']}")
    print("  (Text tokens contain 'united' and 'states' separately!)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 07: text vs keyword Experiments ==="
python3 phases/07-text-vs-keyword/code/text_vs_keyword_demo.py

echo -e "\\n--- Testing Elasticsearch Mappings ---"
curl -s -X PUT "http://localhost:9200/demo_types" -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": { "keyword": { "type": "keyword" } }
      }
    }
  }
}' || true

curl -s -X PUT "http://localhost:9200/demo_types/_doc/1?refresh=true" -H "Content-Type: application/json" -d '{
  "title": "Distributed Systems"
}' || true

echo -e "\\n1. Full-text match query on 'title':"
curl -s -X POST "http://localhost:9200/demo_types/_search" -H "Content-Type: application/json" -d '{
  "query": { "match": { "title": "distributed" } }
}' | grep -o '"total":{"value":[0-9]*' || true

echo -e "\\n2. Exact term query on 'title.keyword':"
curl -s -X POST "http://localhost:9200/demo_types/_search" -H "Content-Type: application/json" -d '{
  "query": { "term": { "title.keyword": "Distributed Systems" } }
}' | grep -o '"total":{"value":[0-9]*' || true
"""),

        (8, "Mappings",
         "Dynamic mapping is convenient in development and fatal in production; explicit schema is engineering discipline.",
         "Demonstrate dynamic mapping type traps and enforce explicit schemas.",
         """# Lesson 08.1: Mappings

## Motto
"Dynamic mapping is convenient in development and fatal in production; explicit schema is engineering discipline."

## Problem
If you index `{"order_id": "00123"}` into an unmapped index, Elasticsearch dynamically infers `long` (number `123`), permanently stripping the leading zeros. When the next document arrives with `{"order_id": "00123-A"}`, indexing fails with a mapping conflict!

## Prediction
What happens when you index a document with dynamic mapping disabled (`dynamic: strict`) containing an undocumented field?

## Why this matters
An Elasticsearch mapping defines the type and indexing rules for every field in an index. Once a field mapping is created in Lucene, it can never be altered or deleted without creating a new index and reindexing all data.

## First principles
Dynamic mapping rules:
* `"2026-01-01"` -> inferred as `date`
* `true` / `false` -> inferred as `boolean`
* `123` -> inferred as `long`
* `"hello"` -> inferred as `text` with `.keyword` multi-field

## Mental model
```text
Dynamic Mapping:
  "0042" ──► Auto-detected as LONG ──► Leading zeros destroyed!

Explicit Mapping:
  "order_id": { "type": "keyword" } ──► Stored as exact string "0042"
```

## Build it
See `code/mapping_simulation.py` illustrating dynamic inference edge cases.

## Use Elasticsearch
Run the experiment:
```bash
./phases/08-mappings/experiments/run_experiment.sh
```

## Inspect it
Retrieve the active mapping of an index:
```bash
curl -s http://localhost:9200/strict_products/_mapping?pretty
```

## Measure it
Compare indexing time: dynamic mapping incurs cluster-state update overhead on new fields, whereas explicit mapping indexes immediately without master node coordination.

## Break it
Configure an index with `"dynamic": "strict"` and index a document containing an unmapped field. Observe the `strict_dynamic_mapping_exception`.

## Recover it
Add the field explicitly to the mapping via `PUT /<index>/_mapping` before indexing.

## Modify it
Set `"dynamic": "runtime"` to evaluate fields dynamically at query time without indexing them.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can existing field types in a mapping never be modified in-place?
2. What is the operational risk of running a production cluster with `dynamic: true`?

## Guarantees
* Explicit mappings strictly enforce data types across all primary and replica shards.

## Non-guarantees
* Elasticsearch does not enforce relational null-checks or cross-field validation.

## When to use this
* Every production index must define an explicit mapping schema.

## When not to use this
* Dynamic mapping should only be used in rapid local prototyping or log collection with unknown formats.

## What comes next
In Phase 09, we trace the full architectural path of an indexing request from HTTP client to disk.
""",
"""#!/usr/bin/env python3

def infer_type(val):
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "long"
    if isinstance(val, float):
        return "double"
    if isinstance(val, str):
        if val.isdigit() and not val.startswith("0"):
            return "long (inferred)"
        return "text + keyword"
    return "object"

if __name__ == "__main__":
    cases = ["00123", "123", "2026-09-23", "true", 42.5]
    print("Simulating Dynamic Field Type Inference:")
    for c in cases:
        print(f"  Input: {repr(c):15s} -> Inferred Type: {infer_type(c)}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 08: Explicit Mappings & Dynamic Traps ==="
python3 phases/08-mappings/code/mapping_simulation.py

echo -e "\\n--- Creating Index with Strict Dynamic Mapping ---"
curl -s -X PUT "http://localhost:9200/strict_products" -H "Content-Type: application/json" -d '{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "sku": { "type": "keyword" },
      "price": { "type": "double" }
    }
  }
}' || true

echo -e "\\n1. Indexing valid document (should succeed):"
curl -s -X POST "http://localhost:9200/strict_products/_doc/1" -H "Content-Type: application/json" -d '{
  "sku": "KB-990",
  "price": 129.99
}' | grep -o '"result":"[^"]*"' || true

echo -e "\\n2. Indexing unexpected field (should fail with strict exception):"
curl -s -X POST "http://localhost:9200/strict_products/_doc/2" -H "Content-Type: application/json" -d '{
  "sku": "KB-991",
  "price": 139.99,
  "unexpected_tag": "sale"
}' | grep -o '"type":"[^"]*"' || true
"""),

        (9, "Indexing Pipeline",
         "From JSON to disk: parse, route, validate against mapping, analyze terms, append to translog, and write segment buffer.",
         "Trace the complete write path of an indexing request.",
         """# Lesson 09.1: Indexing Pipeline

## Motto
"From JSON to disk: parse, route, validate against mapping, analyze terms, append to translog, and write segment buffer."

## Problem
When a client issues `POST /orders/_doc/1`, what actually happens before HTTP 201 Created is returned? Treating this as an atomic database insert hides the dual write to the in-memory indexing buffer and durable transaction log (translog).

## Prediction
Does a successful HTTP 201 Created response mean the document is immediately searchable by concurrent queries?

## Why this matters
Understanding the write pipeline explains write amplification, translog durability, indexing backpressure, and why bulk indexing is drastically faster than individual document inserts.

## First principles
The write pipeline steps:
1. Client sends HTTP POST to any node (Coordinating Node).
2. Coordinating node computes shard: `hash(id) % num_shards`.
3. Request forwarded to Primary Shard node.
4. Primary parses JSON, validates against mapping schema.
5. Analysis pipeline transforms text into terms.
6. Writes to **In-Memory Indexing Buffer** (RAM).
7. Appends operation to **Translog** (disk for durability).
8. Replicates write concurrently to all active Replica Shards.
9. Once primary + replicas acknowledge, HTTP 200/201 response sent to client.

## Mental model
```text
Client
  │ 1. POST /index/_doc/42
  ▼
Coordinating Node
  │ 2. hash("42") % 3 = Shard 1
  ▼
Primary Shard (Node A)
  ├── 3. Parse & Validate Mapping
  ├── 4. Execute Analysis Pipeline
  ├── 5. Write to Lucene Index Buffer (RAM)
  ├── 6. Append to Translog (WAL on disk)
  └── 7. Send write to Replica Shard (Node B)
            │
            ▼
       Replica acknowledges
            │
            ▼
HTTP 201 Created to Client
```

## Build it
See `code/trace_indexing.py` simulating the step-by-step pipeline in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/09-indexing-pipeline/experiments/run_experiment.sh
```

## Inspect it
Inspect the translog generation and uncommitted operations:
```bash
curl -s http://localhost:9200/strict_products/_stats/translog?pretty
```

## Measure it
Measure single-document indexing latency under concurrency.

## Break it
Send invalid JSON or a document violating mapping types and inspect the rejected response.

## Recover it
Correct client payload to match mapping contract.

## Modify it
Toggle the translog sync policy between `request` (sync on every write) and `async` and measure throughput difference.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch write to BOTH an in-memory buffer and a disk translog during indexing?
2. If the node loses power before a refresh occurs, is the indexed document lost?

## Guarantees
* Acknowledged writes are recorded in the translog for crash durability.

## Non-guarantees
* Acknowledged writes are NOT immediately visible to search (until refresh).

## When to use this
* Every document write, update, or bulk ingestion operation.

## When not to use this
* Never use Elasticsearch as an ACID transactional ledger.

## What comes next
In Phase 10, we trace the opposite path: the search and query execution pipeline.
""",
"""#!/usr/bin/env python3
import hashlib

def route_shard(doc_id, num_shards=3):
    # Simplified murmur3-style hash simulation
    h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
    return h % num_shards

def simulate_indexing_pipeline(doc_id, doc, num_shards=3):
    steps = []
    steps.append(f"1. Client issues write request for ID '{doc_id}'")
    shard_id = route_shard(doc_id, num_shards)
    steps.append(f"2. Routed to Primary Shard [{shard_id}] (hash({doc_id}) % {num_shards})")
    steps.append(f"3. Validated fields against schema mapping")
    steps.append(f"4. Executed text analysis: parsed {len(doc)} fields")
    steps.append(f"5. Wrote document terms to in-memory Lucene buffer")
    steps.append(f"6. Appended raw operation to Translog on disk for durability")
    steps.append(f"7. Dispatched operation to replica shard on peer node")
    steps.append(f"8. Returned HTTP 201 Created to client (Segment not yet refreshed!)")
    return steps

if __name__ == "__main__":
    trace = simulate_indexing_pipeline("order-98712", {"item": "Laptop", "price": 1200})
    for s in trace:
        print(s)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 09: Indexing Pipeline Trace ==="
python3 phases/09-indexing-pipeline/code/trace_indexing.py

echo -e "\\n--- Inspecting Translog Stats from Elasticsearch ---"
curl -s -X POST "http://localhost:9200/trace_demo/_doc/1" -H "Content-Type: application/json" -d '{"msg": "trace payload"}' || true
curl -s "http://localhost:9200/trace_demo/_stats/translog?pretty" | grep -E 'operations|size_in_bytes' || true
"""),

        (10, "Search Pipeline",
         "Search is an inverted index scan across immutable segments, scored by relevance and reduced at the coordinator.",
         "Trace query parsing, term lookup, postings intersection, and result retrieval.",
         """# Lesson 10.1: Search Pipeline

## Motto
"Search is an inverted index scan across immutable segments, scored by relevance and reduced at the coordinator."

## Problem
How does Elasticsearch execute a query across multiple shards and millions of documents in 5 milliseconds? Without understanding the two-phase query pipeline, performance tuning is guesswork.

## Prediction
When you ask for `size: 10` on a 5-shard index, do shards send 10 documents each to the coordinator, or do they send full document bodies immediately?

## Why this matters
The query pipeline separates candidate matching and scoring from full document retrieval, minimizing network traffic across cluster nodes.

## First principles
Search executes in two phases:
1. **Query Phase:** Coordinating node scatters query to shards. Each shard queries its Lucene segments, scores matches using BM25, and returns a priority queue of candidate IDs + scores (e.g. top 10).
2. **Fetch Phase:** Coordinating node merges shard queues to find global top 10 winners, then requests full `_source` bodies only for those 10 winning IDs.

## Mental model
```text
                      COORDINATING NODE
                             │
     ┌───────────────────────┴───────────────────────┐
     │ 1. Scatter Query (No docs transferred)        │
     ▼                                               ▼
  SHARD 0                                         SHARD 1
- Postings lookup                               - Postings lookup
- BM25 score                                    - BM25 score
- Returns [Doc 4: 3.2, Doc 9: 2.8]              - Returns [Doc 1: 4.1, Doc 3: 1.5]
     │                                               │
     └───────────────────────┬───────────────────────┘
                             ▼
  2. Merge Top Hits: Overall Winners = [Doc 1 (4.1), Doc 4 (3.2)]
                             │
  3. Fetch Phase: Request full _source only for Doc 1 & Doc 4
                             ▼
  4. Assemble Response -> Send to Client
```

## Build it
See `code/search_pipeline_trace.py` demonstrating query vs fetch phase in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/10-search-pipeline/experiments/run_experiment.sh
```

## Inspect it
Use the `_search` explain parameter to trace term matching and scoring:
```bash
curl -X POST http://localhost:9200/trace_demo/_search?explain=true -H "Content-Type: application/json" -d '{
  "query": { "match": { "msg": "trace" } }
}'
```

## Measure it
Measure query latency with `took` in the response payload.

## Break it
Request `size: 10000` with deep `from: 50000` and observe coordinator memory and network spike.

## Recover it
Switch to `search_after` with Point-in-Time (covered in Phase 57 & 58).

## Modify it
Add `_source: ["msg"]` to request only specific fields during the fetch phase and measure payload size reduction.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch not fetch `_source` during the query phase?
2. What is the network overhead of querying 100 shards versus 2 shards?

## Guarantees
* Query-then-fetch guarantees globally accurate top-$K$ relevance ranking across all shards.

## Non-guarantees
* Exact total hit counts above 10,000 are approximate by default (`relation: "gte"`).

## When to use this
* Standard full-text search and analytical querying.

## When not to use this
* Bulk export of millions of raw records (use Scroll API or sliced `search_after`).

## What comes next
In Phase 11, we explore compound search with Boolean queries (`must`, `filter`, `should`, `must_not`).
""",
"""#!/usr/bin/env python3

def simulate_query_phase(shards_data, query_term, top_k=2):
    # Phase 1: Query Phase (returns only doc_id and score)
    shard_results = {}
    for shard_id, docs in shards_data.items():
        candidates = []
        for doc_id, text in docs.items():
            if query_term in text.lower():
                score = round(1.0 + (len(text) % 3) * 0.5, 2)
                candidates.append((doc_id, score))
        candidates.sort(key=lambda x: x[1], reverse=True)
        shard_results[shard_id] = candidates[:top_k]
    return shard_results

def simulate_fetch_phase(shards_data, winning_ids):
    # Phase 2: Fetch Phase (retrieves full body only for winning IDs)
    docs = {}
    for shard_id, shard_docs in shards_data.items():
        for doc_id in winning_ids:
            if doc_id in shard_docs:
                docs[doc_id] = shard_docs[doc_id]
    return docs

if __name__ == "__main__":
    cluster_shards = {
        "shard_0": {101: "Elasticsearch distributed cluster", 102: "Kafka streaming log"},
        "shard_1": {201: "Elasticsearch fast inverted index", 202: "Redis in-memory store"}
    }
    print("--- Phase 1: Query Phase ---")
    shard_candidates = simulate_query_phase(cluster_shards, "elasticsearch", top_k=2)
    print("Shard candidate scores:", shard_candidates)

    all_candidates = []
    for s_hits in shard_candidates.values():
        all_candidates.extend(s_hits)
    all_candidates.sort(key=lambda x: x[1], reverse=True)
    top_winners = [doc_id for doc_id, score in all_candidates[:2]]
    print("Top global winners:", top_winners)

    print("\\n--- Phase 2: Fetch Phase ---")
    fetched = simulate_fetch_phase(cluster_shards, top_winners)
    print("Fetched documents:", fetched)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 10: Search Pipeline Simulation ==="
python3 phases/10-search-pipeline/code/search_pipeline_trace.py

echo -e "\\n--- Running Search on Elasticsearch ---"
curl -s -X POST "http://localhost:9200/trace_demo/_search" -H "Content-Type: application/json" -d '{
  "query": { "match_all": {} },
  "size": 2
}' | grep -o '"hits":\[.*\]' || true
""")
    ]

    for p_num, p_title, motto, problem, doc_content, code_content, exp_content in phases:
        slug = f"{p_num:02d}-{p_title.lower().replace(' ', '-').replace('/', '-')}"
        phase_dir = os.path.join(PHASES_DIR, slug)
        write_file(os.path.join(phase_dir, "docs", "en.md"), doc_content)
        write_file(os.path.join(phase_dir, "code", f"{slug.replace('-', '_')}.py"), code_content)
        write_file(os.path.join(phase_dir, "experiments", "run_experiment.sh"), exp_content)
        write_file(os.path.join(phase_dir, "outputs", "evidence-template.md"), evidence_template(p_title, p_num))
        print(f"Generated Phase {p_num:02d}: {p_title}")

if __name__ == "__main__":
    generate_phases_00_to_25()
