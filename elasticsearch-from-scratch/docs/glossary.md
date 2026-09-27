# Elasticsearch & Information Retrieval Glossary

A precise, first-principles glossary for search engine engineering and distributed data systems.

---

### Inverted Index
A data structure mapping every distinct word (term) to the list of document IDs (postings list) that contain it, along with term positions and frequencies. Enables sub-millisecond full-text lookup without scanning document bodies sequentially.

### Tokenization
The process of breaking a raw sequence of characters into individual discrete semantic tokens (words, n-grams, or symbols), discarding whitespace and specified delimiters.

### Text Analysis
The end-to-end pipeline that transforms raw unstructured text into searchable inverted index terms. Consists of zero or more **Character Filters**, exactly one **Tokenizer**, and zero or more **Token Filters**.

### Character Filter
The first stage of an analyzer. Operates on raw characters before tokenization. Examples: HTML strip filter (`html_strip`), regex pattern replace filter, character mapping.

### Tokenizer
The core stage of an analyzer that divides character streams into discrete tokens while recording token offsets and positions. Examples: `standard`, `whitespace`, `keyword`, `pattern`.

### Token Filter
The final stage of an analyzer that modifies, removes, or enriches tokens emitted by a tokenizer. Examples: `lowercase`, `stop`, `synonym`, `stemmer`, `edge_ngram`.

### `text` Field Type
An Elasticsearch data type designed for unstructured, human-readable full-text search. The string is analyzed and tokenized into an inverted index. Sorting and aggregations are disabled by default (due to memory costs of fielddata).

### `keyword` Field Type
An Elasticsearch data type designed for structured, exact-match values (e.g. status codes, country names, UUIDs). The string is indexed verbatim without analysis and stored in columnar **Doc Values** for fast sorting, filtering, and aggregations.

### Multi-Field
A mapping configuration allowing a single JSON field to be indexed in multiple ways (e.g., as analyzed `text` for full-text search and as `keyword` for exact filtering and aggregations).

### Mapping
The schema definition of an index that specifies field names, their data types (`text`, `keyword`, `long`, `date`, `geo_point`, `dense_vector`), analyzers, and index options. Can be explicit or dynamically inferred.

### Dynamic Mapping
Elasticsearch's capability to automatically infer and generate field types when unmapped fields are encountered in an indexed document. Convenient for prototyping, dangerous in production due to mapping explosions and inaccurate type inferences.

### Mapping Explosion
A catastrophic operational failure where an index acquires tens of thousands of dynamic fields (e.g., dynamically using user IDs as JSON keys), causing massive JVM heap consumption to maintain the cluster state and eventual cluster collapse.

### Lucene Segment
An immutable, self-contained physical index directory on disk containing an inverted index, columnar doc values, stored fields, and term vectors. A shard consists of multiple Lucene segments.

### Segment Immutability
The design property that once written and flushed to disk, a Lucene segment is never modified in place. Updates and deletes are handled by creating new segments and writing a bitset of deleted document IDs (`.del` files). Enables concurrent lock-free reads and efficient OS page caching.

### Refresh
The operation that flushes recently indexed documents from in-memory index buffers into a new, searchable Lucene segment in the OS filesystem cache. By default occurs every 1 second (`refresh_interval`), giving Elasticsearch its **Near-Real-Time (NRT)** property.

### Flush & Translog (Transaction Log)
The operation that writes all Lucene segments from OS page cache down to physical disk (calling `fsync`) and empties the Lucene commit transaction log (`translog`). Guarantees durability across power outages and crashes.

### Segment Merge
The background housekeeping process that consolidates multiple small immutable segments into fewer, larger segments, physically purging documents marked as deleted to reclaim disk space and reduce search file-handle overhead.

### Near-Real-Time (NRT)
The architectural property where newly indexed documents are acknowledged before they are searchable, becoming visible to queries only after the next `refresh` creates a searchable segment.

### BM25 (Best Matching 25)
The default probabilistic relevance ranking algorithm in Elasticsearch and Lucene. Scores documents based on Term Frequency (TF) with saturation ($k_1$), Inverse Document Frequency (IDF), and Field Length Normalization ($b$).

### Term Frequency (TF)
The number of times a search term appears in a specific document. In BM25, higher term frequency increases the relevance score, but with diminishing marginal returns (saturation controlled by parameter $k_1$).

### Inverse Document Frequency (IDF)
A measure of how rare or informative a term is across the entire corpus. Calculated as $\ln(1 + \frac{N - n + 0.5}{n + 0.5})$ where $N$ is total documents and $n$ is documents containing the term. Rare terms yield high IDF; ubiquitous terms yield near-zero IDF.

### Field Length Normalization
The mechanism in BM25 that penalizes long fields and rewards short fields. A matching term in a 5-word title provides stronger relevance signal than the same term in a 1,000-word article body. Controlled by parameter $b$ (default 0.75).

### Query Context vs. Filter Context
* **Query Context:** The clause answers *"How well does this document match the query?"* Documents are scored and ranked using BM25 relevance scores.
* **Filter Context:** The clause answers *"Does this document match the criteria?"* A binary yes/no evaluation without scoring. Results are deterministic, score is $0.0$, and results can be cached automatically in the Node Query Cache.

### Bool Query
A composite query combining multiple clauses:
* `must`: Clause must match; contributes to relevance score.
* `filter`: Clause must match; does not contribute to score; eligible for caching.
* `should`: Optional match; increases score if matched; can enforce minimum matches (`minimum_should_match`).
* `must_not`: Must not match; executed in filter context (no score contribution).

### Aggregations
Distributed analytics framework executing map-reduce style operations across candidate documents. Divided into:
* **Bucket Aggregations:** Partition documents into sets (e.g. `terms`, `date_histogram`, `range`).
* **Metric Aggregations:** Compute values across buckets (e.g. `avg`, `sum`, `min`, `max`, `cardinality`, `percentiles`).

### Shard
An independent, fully functional Lucene index instance. An Elasticsearch index is logically partitioned into one or more primary shards distributed across cluster nodes to scale storage and throughput.

### Primary Shard
The authoritative shard that sequences and coordinates write operations (indexing, updating, deleting) before replicating them to replica shards.

### Replica Shard
An exact copy of a primary shard that provides high-availability failover if the primary node crashes, and scales read query throughput by serving concurrent search requests.

### Coordinating Node
The node that receives an incoming search or indexing request from a client. For search, it acts as a scatter-gather coordinator, routing sub-queries to shards and reducing the aggregated response.

### Document Routing
The mathematical formula determining which shard stores a document:
$$\text{shard} = \text{hash}(\text{routing\_value}) \pmod{\text{number\_of\_primary\_shards}}$$
By default, `routing_value` is the document's `_id`. Custom routing (`_routing`) can co-locate related documents on a single shard.

### Hot Shard
A shard that receives an abnormally high share of search or indexing load (often caused by poor routing or skewed key distributions), bottlenecking overall cluster throughput.

### Oversharding
The anti-pattern of creating far too many tiny shards (e.g., hundreds of shards for a few gigabytes of data). Each shard consumes JVM heap for segment metadata and adds coordination latency to queries.

### Cluster State
The global metadata coordinated by the active master node, describing node membership, index settings, mappings, shard routing tables, and allocation status.

### Cluster Health States
* **Green:** All primary and replica shards are successfully assigned to active nodes.
* **Yellow:** All primary shards are active, but one or more replica shards are unassigned (data safe, redundancy reduced).
* **Red:** At least one primary shard is unassigned and offline (data loss or partial search unavailability).

### Doc Values
A disk-backed, columnar data structure built at index time alongside the inverted index for non-analyzed fields (`keyword`, `numeric`, `date`, `boolean`, `geo_point`). Allows memory-efficient sorting, aggregations, and script access without loading analyzed strings into the JVM heap.

### Fielddata
An in-memory, column-oriented data structure generated on the fly by un-inverting the inverted index in JVM heap memory. Required only if executing aggregations or sorting on analyzed `text` fields. Disabled by default because it quickly triggers OutOfMemory errors.

### `_source`
The original, untouched JSON document payload stored as a single compressed byte block inside Lucene. Used for retrieving original document contents upon search hits, highlights, and reindexing. Does not participate in term lookup.
