# Curriculum Roadmap: `elasticsearch-from-scratch`

> **Motto:** Understand it. Build it. Index it. Search it. Measure it. Break it. Recover it. Scale it. Ship it.

This roadmap details all 88 phases across 9 milestones. Every phase is dependency-ordered, runnable, measurable, and evidence-producing.

---

## Milestone 1: Foundations of Search & Indexing (Phases 00–12)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **00** | Environment & Search Lab | None | REST API, TCP 9200/9300, Single Node | Inspect cluster root ping & health | `check_node.py` | Explain 9200 vs 9300 ports |
| **01** | Why Search Engines Exist | Phase 00 | $O(N)$ Table Scan vs $O(1)$ Search | Benchmark linear scan vs index | `linear_vs_index.py` | Explain B-Tree prefix limitation |
| **02** | Build an Inverted Index | Phase 01 | Postings Lists, Term-Doc Mapping | Inverted index lookup vs scan | `mini_search.py` | Explain why postings are sorted |
| **03** | Tokenization | Phase 02 | Token Boundaries, Offsets, Punctuation | Standard vs whitespace tokenizer | `tokenizer_experiments.py` | Explain character loss trade-offs |
| **04** | Normalization | Phase 03 | Lowercase, Stop Words, Porter Stemming | Stemming recall vs precision | `normalizer.py` | Explain stemming over-generalization |
| **05** | Analyzer Pipeline | Phase 04 | Char Filters $\to$ Tokenizer $\to$ Token Filters | Inline custom `_analyze` pipeline | `custom_analyzer_test.py` | Explain why only 1 tokenizer exists |
| **06** | Documents and Fields | Phase 05 | Per-Field Indexing, Field Types | Fielded search vs global search | `fielded_search.py` | Explain string vs numeric sorting |
| **07** | text vs keyword | Phase 06 | Analyzed Text vs Columnar Doc Values | Multi-fields (`title.keyword`) | `text_vs_keyword_demo.py` | Explain why term search on text fails |
| **08** | Mappings | Phase 07 | Dynamic Inference vs Explicit Schema | Strict dynamic mapping validation | `mapping_simulation.py` | Explain why mappings are immutable |
| **09** | Indexing Pipeline | Phase 08 | Routing, Buffer, Translog, Replication | Trace step-by-step write path | `trace_indexing.py` | Explain role of Translog |
| **10** | Search Pipeline | Phase 09 | Scatter-Gather, Query Phase, Fetch Phase | Simulate two-phase query execution | `search_pipeline_trace.py` | Explain why _source is fetched last |
| **11** | Boolean Search | Phase 10 | Must, Filter, Should, Must_Not | Compose multi-clause bool query | `11_boolean_search.py` | Explain should as score booster |
| **12** | Query vs Filter | Phase 11 | Scoring Context vs Cached Filter Bitset | Inspect `_score: 0.0` vs BM25 score | `12_query_vs_filter.py` | Explain bitset caching mechanism |

---

## Milestone 2: Information Retrieval & Relevance (Phases 13–20)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **13** | Ranking From Scratch | Phase 12 | Term Count, Document Length Normalization | Compare raw count vs density score | `13_ranking_from_scratch.py` | Explain keyword stuffing hazard |
| **14** | TF-IDF Intuition | Phase 13 | Inverse Document Frequency, Rarity | Calculate IDF across multi-doc corpus | `14_tf_idf_intuition.py` | Explain logarithmic scale in IDF |
| **15** | BM25 | Phase 14 | TF Saturation ($k_1$), Length Norm ($b$) | Plot TF saturation curve | `15_bm25.py` | Explain why BM25 saturates |
| **16** | Explain Relevance | Phase 15 | Score Decomposition, Lucene Weights | Inspect `_explain` scoring tree | `16_explain_relevance.py` | Audit BM25 term scores |
| **17** | Phrase Search | Phase 16 | Positional Postings, Slop Distance | Positional index vs bag-of-words | `17_phrase_search.py` | Explain position storage cost |
| **18** | Prefix, Wildcard, Regex | Phase 17 | FST Lexicographical Dictionary Scan | Benchmark prefix vs `*search*` | `18_prefix_wildcard.py` | Explain leading wildcard penalty |
| **19** | Fuzzy Search | Phase 18 | Damerau-Levenshtein Edit Distance | Auto fuzziness on typos | `19_fuzzy_search.py` | Distinguish typo vs semantics |
| **20** | Synonyms | Phase 19 | Synonym Graph, Index vs Search Time | Test search-time synonym expansion | `20_synonyms.py` | Explain why search-time is preferred |

---

## Milestone 3: Autocomplete & Data Type Systems (Phases 21–25)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **21** | Autocomplete | Phase 20 | Prefix Query vs Edge N-grams vs FST | Suggest latency vs memory | `21_autocomplete.py` | Explain JVM FST heap cost |
| **22** | N-grams | Phase 21 | Substring Token Expansion, Disk Bloat | Measure term count multiplication | `22_n_grams.py` | Calculate index growth factor |
| **23** | Search-As-You-Type | Phase 22 | 2-gram/3-gram Shingles, Prefix Match | Multi-field search-as-you-type | `23_search_as_you_type_design.py` | Explain shingle subfield roles |
| **24** | Numeric and Date Fields | Phase 23 | BKD Trees, Multi-Dimensional Points | Benchmark 1D range queries | `24_numeric_and_date_fields.py` | Contrast BKD tree vs inverted index |
| **25** | Geo Search | Phase 24 | Spatial Coordinates, Haversine Distance | Bounding box vs distance radius | `25_geo_search.py` | Explain spherical distance calculation |

---

## Milestone 4: Distributed Aggregations & Storage Internals (Phases 26–33)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **26** | Aggregations First Principles | Phase 25 | Map-Reduce Faceting, Hits vs Aggs | Group-by count and average in Python | `26_aggregations_from_first_principles.py` | Explain `size: 0` optimization |
| **27** | Bucket Aggregations | Phase 26 | Terms, Date Histogram, Ranges | Partition catalog into facets | `27_bucket_aggregations.py` | Explain distributed terms approximation |
| **28** | Metric Aggregations | Phase 27 | Stats, HyperLogLog++, T-Digest | Approximate cardinality vs exact set | `28_metric_aggregations.py` | Explain HLL++ constant memory |
| **29** | Nested Aggregations | Phase 28 | Multi-Tier Hierarchical Cubes | Category $\to$ Brand $\to$ Avg Price | `29_nested_aggregations.py` | Explain combinatorial explosion risk |
| **30** | Arrays & Nested Fields | Phase 29 | Object Flattening Bug vs `nested` Type | Cross-object false match demonstration | `30_arrays_objects_nested.py` | Explain why standard arrays flatten |
| **31** | Source vs Index | Phase 30 | `_source` Store, Inverted Index, Doc Values | Disable `_source` and observe impacts | `31_source_vs_index.py` | Explain why reindex needs `_source` |
| **32** | Doc Values | Phase 31 | Columnar Disk Storage, OS Page Cache | Benchmark row scan vs column scan | `32_doc_values.py` | Explain why doc values bypass JVM heap |
| **33** | Fielddata | Phase 32 | In-Memory Un-Inversion, Circuit Breaker | Trap `text` field aggregation error | `33_fielddata.py` | Explain why fielddata causes OOM |

---

## Milestone 5: Lucene Segments & Write Architecture (Phases 34–41)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **34** | Segments | Phase 33 | Immutable Segments, Lock-Free Reads | Search across multiple segments | `34_segments.py` | Explain why segments never mutate |
| **35** | Near-Real-Time Search | Phase 34 | Acknowledgment vs Search Visibility | Demonstrate 1-second refresh lag | `35_near_real_time_search.py` | Explain NRT vs immediate search |
| **36** | Refresh | Phase 35 | Memory Buffer $\to$ OS Cache Segment | Benchmark 1s vs 30s refresh interval | `36_refresh.py` | Explain `?refresh=true` cost |
| **37** | Flush and Durability | Phase 36 | Translog WAL, `fsync()`, Commit Points | Flush translog to disk | `37_flush_and_durability.py` | Distinguish Refresh from Flush |
| **38** | Segment Merging | Phase 37 | Tiered Merge Policy, Purging `.del` | Force-merge small segments to 1 | `38_segment_merging.py` | Explain why delete increases disk |
| **39** | Updates and Deletes | Phase 38 | Soft Delete Tombstone + Insert | Track `docs.deleted` during updates | `39_updates_and_deletes.py` | Explain write amplification |
| **40** | Bulk Indexing | Phase 39 | NDJSON Streaming, HTTP Roundtrips | Benchmark 1 doc/req vs bulk batches | `40_bulk_indexing.py` | Explain why NDJSON is preferred |
| **41** | Indexing Throughput | Phase 40 | Bulk Size, Refresh, Concurrency, Replicas | Maximize write throughput to hardware | `41_indexing_throughput.py` | Identify write bottleneck |

---

## Milestone 6: Distributed Sharding & Resilience (Phases 42–55)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **42** | Sharding First Principles | Phase 41 | Partitioning, Shard == Lucene Index | Hash partitioning into 3 shards | `42_sharding_from_first_principles.py` | Explain why shard count is fixed |
| **43** | Document Routing | Phase 42 | Hash Routing, Custom `_routing` | Single-shard targeted query vs broadcast | `43_document_routing.py` | Explain fan-out elimination |
| **44** | Distributed Search | Phase 43 | Coordinating Node, Scatter-Gather | Multi-shard scatter-gather simulation | `44_distributed_search.py` | Explain slow-shard tail latency |
| **45** | Query Then Fetch | Phase 44 | Two-Phase Search, Payload Transfer | Compare payload bytes vs eager fetch | `45_query_then_fetch.py` | Explain two roundtrips benefit |
| **46** | Shard Count | Phase 45 | Shard Sizing (20GB - 50GB Guideline) | Benchmark 1 shard vs 10 shards | `46_shard_count.py` | Explain small data oversharding penalty |
| **47** | Oversharding | Phase 46 | Heap Overhead per Shard, File Handles | Calculate static heap waste | `47_oversharding.py` | State recommended shards/GB ratio |
| **48** | Replicas | Phase 47 | Failover, Read Load Balancing | Scale read QPS with replica copies | `48_replicas.py` | Explain primary vs replica roles |
| **49** | Node Failure | Phase 48 | Heartbeat Timeout, Promotion, Peer Sync | Kill node and observe live failover | `49_node_failure.py` | Explain automatic promotion |
| **50** | Cluster Health | Phase 49 | Green, Yellow, Red Diagnostic Meaning | Cause and heal yellow state | `50_cluster_health.py` | Explain data safety under Yellow |
| **51** | Shard Allocation | Phase 50 | Allocation Deciders, `same_shard` | Run `_cluster/allocation/explain` | `51_shard_allocation.py` | Diagnose unassigned shards |
| **52** | Cluster State | Phase 51 | Master Node Coordination, State Diffs | Track cluster state version updates | `52_cluster_state.py` | Explain metadata serialization lag |
| **53** | Mapping Explosion | Phase 52 | Dynamic Keys Hazard, `total_fields` Limit | Trigger and prevent field explosions | `53_mapping_explosion.py` | Defend against dynamic keys |
| **54** | High Cardinality | Phase 53 | UUID Aggregations, Memory Footprint | Measure grouping across 50,000 unique keys | `54_high_cardinality.py` | Tune `shard_size` parameter |
| **55** | Hot Shards | Phase 54 | Load Skew, Unbalanced Routing | Diagnose hot threads on stressed node | `55_hot_shards.py` | Balance partition key distribution |

---

## Milestone 7: Performance, Operations & Resilience (Phases 56–68)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **56** | Search Caching | Phase 55 | Node Query Cache, Shard Request Cache | Measure filter bitset cache speedup | `56_search_caching.py` | Explain what invalidates query cache |
| **57** | Pagination | Phase 56 | Deep Paging Penalty, `search_after` | Benchmark `from` vs cursor pagination | `57_pagination.py` | Explain $O(N)$ deep paging penalty |
| **58** | Point in Time | Phase 57 | Consistent Snapshot Views, PIT Tokens | Paginate across active background writes | `58_point_in_time.py` | Explain why PIT retains segments |
| **59** | Sorting | Phase 58 | Score Sort vs Doc Values Sort, Index Sort | Measure early termination speedup | `59_sorting.py` | Explain `_score: null` during sort |
| **60** | Slow Queries | Phase 59 | Wildcard Scans, Search Slow Logs | Configure slow log thresholds | `60_slow_queries.py` | Audit expensive query patterns |
| **61** | Search Profiling | Phase 60 | Profile API, Lucene Scorer Breakdown | Dissect nanosecond query execution | `61_search_profiling.py` | Identify query phase bottlenecks |
| **62** | Indexing Backpressure | Phase 61 | Write Queue Overflow, HTTP 429 | Exponential backoff with jitter | `62_indexing_backpressure.py` | Explain why write queue is bounded |
| **63** | Heap and Memory | Phase 62 | JVM Heap (31GB Max) vs OS Page Cache | Calculate Compressed OOPs penalty | `63_heap_and_memory.py` | Defend the 50% RAM rule |
| **64** | Disk and Watermarks | Phase 63 | 85% Low, 90% High, 95% Flood Stage Lock | Clear `read_only_allow_delete` block | `64_disk_and_watermarks.py` | Explain flood stage safety |
| **65** | Snapshots and Restore | Phase 64 | Replicas $\neq$ Backups, Incremental Snaps | Delete index and restore from snapshot | `65_snapshots_and_restore.py` | Explain incremental segment backup |
| **66** | Index Lifecycle (ILM) | Phase 65 | Hot, Warm, Cold, Delete Data Tiers | Configure automated rollover policy | `66_index_lifecycle_concepts.py` | Explain warm force-merge benefit |
| **67** | Time-Series Workload | Phase 66 | Rolling Daily Indices vs Monolithic Index | Date histogram error analysis | `67_time_series_logging.py` | Explain $O(1)$ index drop vs delete |
| **68** | Ingest Pipelines | Phase 67 | Grok Parsing, GeoIP, Date Transformations | Preprocess raw logs with `_simulate` | `68_ingest_pipelines.py` | Contrast cluster vs client ETL |

---

## Milestone 8: Capstones, Security & Engineering (Phases 69–81)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **69** | Search API Design | Phase 68 | Gateway Translation, Preventing DSL Leaks | Build sanitized search gateway | `69_search_api_design.py` | Explain multi-tenant filter injection |
| **70** | Product Search Project | Phase 69 | **Capstone 1:** E-Commerce Catalog Search | Full e-commerce search with facets & typos | `projects/product_search/` | Measure p95 search latency |
| **71** | Log Search Project | Phase 70 | **Capstone 2:** Microservices APM Log Search | Error aggregation & trace correlation | `projects/log_search/` | Extract top root cause exceptions |
| **72** | Search Relevance Eval | Phase 71 | Precision@K, Mean Reciprocal Rank, NDCG | Quantitative test suite evaluation | `72_search_relevance_evaluation.py` | Calculate MRR improvement |
| **73** | Synonym & Relevance Tuning | Phase 72 | Field Boosting, Cross-Fields Matching | Maximize relevance score accuracy | `73_synonym_and_relevance_tuning.py` | Prevent boost over-fitting |
| **74** | Reindexing | Phase 73 | Schema Migration, `_reindex` API | Cast field types from v1 to v2 | `74_reindexing.py` | Explain why reindex is required |
| **75** | Aliases & Zero-Downtime | Phase 74 | Atomic Alias Swap, Zero Downtime | Swap alias pointer in 0.001 ms | `75_aliases_and_zero_downtime_index_migration.py` | Execute zero-downtime migration |
| **76** | Security Basics | Phase 75 | Transport TLS, HTTP TLS, RBAC Roles | Enforce read-only index privileges | `76_elasticsearch_security_basics.py` | Explain transport vs client TLS |
| **77** | Observability | Phase 76 | QPS, Latency p95, Heap %, Rejections | Build automated health evaluator | `77_observability.py` | Identify leading crash indicator |
| **78** | Capacity Planning | Phase 77 | Storage Formulas, Shard & RAM Math | Plan cluster for 200 GB/day workload | `78_capacity_planning.py` | Calculate physical disk required |
| **79** | Failure Scenarios | Phase 78 | Chaos Drills: 7 Canonical Outages | Systematically inject & recover failures | `79_failure_scenarios.py` | Demonstrate live recovery |
| **80** | Build Mini Search Engine | Phase 79 | **Capstone 3:** Standalone Search Engine | Pure Python inverted index + BM25 engine | `projects/mini_search_engine/` | Explain internal architecture |
| **81** | Distributed Simulator | Phase 80 | Multi-Shard Coordination Simulator | Scatter-gather with tail latency injection | `projects/distributed_simulator/` | Explain partial hit tolerance |

---

## Milestone 9: Architectural Synthesis & System Design (Phases 82–87)

| Phase | Title | Prerequisite | Key Concepts | Main Experiment | Artifact | Mastery Check |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **82** | Elasticsearch vs Database | Phase 81 | B-Tree vs Inverted Index, ACID vs NRT | Workload decision trade-off matrix | `82_elasticsearch_vs_database.py` | Explain when Postgres wins |
| **83** | Elasticsearch vs Vector | Phase 82 | BM25 Lexical vs Dense Vector $k$-NN | Hybrid search with Reciprocal Rank Fusion | `83_elasticsearch_vs_vector_search.py` | Explain vector SKU failure |
| **84** | Anti-Patterns | Phase 83 | The 15 Fatal Search Engine Mistakes | Audit lab cluster for design risks | `84_elasticsearch_anti_patterns.py` | Explain replica backup fallacy |
| **85** | When NOT to Use ES | Phase 84 | Primary OLTP, FIFO Queues, Tiny Datasets | Technology selection boundaries | `85_when_elasticsearch_is_the_wrong_tool.py` | Explain why ES fails as a queue |
| **86** | System Design Scenarios | Phase 85 | 8 Enterprise Production Architectures | Answer 20 questions for real systems | `86_system_design_with_elasticsearch.py` | Design end-to-end catalog search |
| **87** | Final Mental Model | Phase 86 | Grand Synthesis: Full Write & Search Trace | Complete trace: `POST /_doc` to disk & `GET /_search` | `87_final_mental_model.py` | Trace complete document life |
