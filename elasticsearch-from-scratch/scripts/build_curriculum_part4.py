#!/usr/bin/env python3
"""
build_curriculum_part4.py - Generates Phases 42 to 55 for elasticsearch-from-scratch.
Covers Sharding, Document Routing, Distributed Search, Replicas, Node Failure, Cluster Health,
Shard Allocation, Cluster State, Mapping Explosion, High Cardinality, and Hot Shards.
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

def generate_phases_42_to_55():
    phases = [
        (42, "Sharding From First Principles",
         "A shard is an independent Lucene index: partitioning allows an index to exceed the storage and compute of a single machine.",
         """# Lesson 42.1: Sharding From First Principles

## Motto
"A shard is an independent Lucene index: partitioning allows an index to exceed the storage and compute of a single machine."

## Problem
A single node with a 2TB disk and 32GB RAM cannot hold a 10TB search corpus. Even if disk was infinite, a single CPU cannot process queries across 1 billion documents with sub-second latency.

## Prediction
Can an index with 3 primary shards be distributed across 3 distinct physical servers, with each server executing query work in parallel?

## Why this matters
Sharding is the horizontal scaling engine of Elasticsearch. Understanding that **a shard is literally an independent Apache Lucene index directory** demystifies distributed search.

## First principles
* **Index vs Shard:** An Index is a logical namespace; a Shard is a physical Lucene index instance.
* Sharding divides documents across $N$ primary shards.
* Adding nodes allows shards to spread out, distributing CPU, memory, and disk I/O.

## Mental model
```text
Logical Index: "logs-2026" (10 TB total)
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 Shard 0    Shard 1    Shard 2
 (3.3 TB)   (3.3 TB)   (3.3 TB)
 [Node 1]   [Node 2]   [Node 3]
```

## Build it
See `code/shard_partition_sim.py` demonstrating hash partitioning of documents into distinct independent Lucene-like indices in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/42-sharding-from-first-principles/experiments/run_experiment.sh
```

## Inspect it
Create an index with 3 primary shards and inspect their physical assignment:
```bash
curl -X PUT http://localhost:9200/sharded_index -H "Content-Type: application/json" -d '{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  }
}'
curl -s "http://localhost:9200/_cat/shards/sharded_index?v"
```

## Measure it
Inspect document distribution across the 3 shards using `_cat/shards`.

## Break it
Try to change `number_of_shards` from 3 to 4 on an existing index using `PUT /sharded_index/_settings`.
**Observed Error:** `"Cannot change primary shards for an open index."`

## Recover it
Primary shard count is immutable after index creation because document routing depends on the modulo of shard count! To change shard count, you must `_split`, `_shrink`, or create a new index and `_reindex`.

## Modify it
Inspect shard sizes on disk via `_cat/shards?v&h=index,shard,prirep,state,docs,store`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is a shard described as an "independent Lucene index"?
2. Why can you dynamically change `number_of_replicas` but NOT `number_of_shards`?

## Guarantees
* Sharding allows an index to store and query more data than can fit on any single physical server.

## Non-guarantees
* Adding more shards does not automatically make queries faster (fan-out coordination overhead).

## When to use this
* Scaling dataset storage and indexing capacity across multiple nodes.

## When not to use this
* Small datasets (< a few GB): a single primary shard is faster and consumes far less memory.

## What comes next
In Phase 43, we analyze Document Routing: how Elasticsearch decides which shard stores which document.
""",
"""#!/usr/bin/env python3
import hashlib

class ShardedIndexSim:
    def __init__(self, num_shards=3):
        self.num_shards = num_shards
        # Each shard is an independent inverted index
        self.shards = {i: {} for i in range(num_shards)}

    def route(self, doc_id):
        # Deterministic hash routing formula
        h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
        return h % self.num_shards

    def index(self, doc_id, text):
        target_shard = self.route(doc_id)
        self.shards[target_shard][doc_id] = text
        return target_shard

if __name__ == "__main__":
    cluster = ShardedIndexSim(num_shards=3)
    docs = [("item_1", "wireless mouse"), ("item_2", "gaming keyboard"), ("item_3", "hdmi cable"), ("item_4", "desk mat")]
    print("Indexing documents into 3 shards:")
    for d_id, text in docs:
        shard_id = cluster.index(d_id, text)
        print(f"  Doc '{d_id}' -> Assigned to Shard [{shard_id}]")

    print("\\nShard Contents:")
    for s_id, s_docs in cluster.shards.items():
        print(f"  Shard {s_id}: {list(s_docs.keys())}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 42: Sharding From First Principles ==="
python3 phases/42-sharding-from-first-principles/code/42_sharding_from_first_principles.py
"""),

        (43, "Document Routing",
         "Shard = hash(routing_value) % num_primary_shards: custom routing eliminates scatter-gather by isolating searches to one shard.",
         """# Lesson 43.1: Document Routing

## Motto
"Shard = hash(routing_value) % num_primary_shards: custom routing eliminates scatter-gather by isolating searches to one shard."

## Problem
In a multi-tenant SaaS application with 10,000 corporate customers, every customer search queries ALL shards across the entire cluster (scatter-gather). Even though Customer 42's data is only 10MB, the query wastes resources hitting 20 different nodes!

## Prediction
Can you force all documents belonging to a specific customer to live on the exact same shard, so customer queries only hit a single shard?

## Why this matters
The default routing formula is:
$$\text{shard} = \text{hash}(\text{_id}) \pmod{\text{number\_of\_primary\_shards}}$$
By supplying a custom routing key (`_routing`), you can co-locate related documents on one shard, eliminating distributed network fan-out!

## First principles
* **Default Routing:** Uniform hash distribution across all shards. Great for balanced disk usage, but requires scatter-gather across all shards for searches.
* **Custom Routing (`?routing=tenant_123`):** Hashes the routing value instead of `_id`. All documents for that tenant land on the exact same shard.
* Searches with `?routing=tenant_123` hit **exactly one shard**!

## Mental model
```text
Default Search:
  GET /orders/_search?q=laptop
  Coordinating Node ──► Scatter to Shard 0, Shard 1, Shard 2 (All Shards!)

Custom Routing Search:
  GET /orders/_search?routing=tenant_42&q=laptop
  Coordinating Node ──► Hits ONLY Shard 1! (Zero Fan-Out!)
```

## Build it
See `code/custom_routing_sim.py` demonstrating single-shard targeted queries vs multi-shard broadcast.

## Use Elasticsearch
Run the experiment:
```bash
./phases/43-document-routing/experiments/run_experiment.sh
```

## Inspect it
Index documents with custom routing and verify shard placement:
```bash
curl -X PUT "http://localhost:9200/routing_demo/_doc/1?routing=company_a" -H "Content-Type: application/json" -d '{"company": "company_a", "val": 100}'
curl -X PUT "http://localhost:9200/routing_demo/_doc/2?routing=company_a" -H "Content-Type: application/json" -d '{"company": "company_a", "val": 200}'
```
Query with `_search?routing=company_a` and check `_shards.total: 1` in the response header!

## Measure it
Compare query QPS: targeted single-shard searches can achieve 5x to 10x higher cluster throughput than scatter-gather queries.

## Break it
Route 90% of all data to a single tenant key (`routing=uber_tenant`). That single shard becomes a massive **Hot Shard**, while other shards sit idle!

## Recover it
Use `index.routing_partition_size` to spread a custom routing key across a bounded subset of shards.

## Modify it
Enforce mandatory routing in the mapping: `"_routing": { "required": true }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does changing the number of primary shards break document routing?
2. What is the risk of using custom routing with an uneven data distribution?

## Guarantees
* Custom routing guarantees all documents sharing a routing key are stored on the same shard.

## Non-guarantees
* Custom routing does not guarantee balanced disk space across nodes if tenant sizes vary wildly.

## When to use this
* Multi-tenant SaaS architectures, user-partitioned social feeds, and time-series session stores.

## When not to use this
* Public global catalogs where queries span all items globally.

## What comes next
In Phase 44, we trace Distributed Search: scatter-gather query coordination across nodes.
""",
"""#!/usr/bin/env python3
import hashlib

def get_shard(routing_key, num_shards=5):
    h = int(hashlib.md5(str(routing_key).encode()).hexdigest(), 16)
    return h % num_shards

if __name__ == "__main__":
    num_shards = 5
    tenants = ["acme_corp", "globex", "initech", "umbrella_corp"]
    print(f"Cluster with {num_shards} Primary Shards:\\n")
    for t in tenants:
        shard = get_shard(t, num_shards)
        print(f"Tenant '{t:15s}' ──► Routed exclusively to Shard [{shard}]")
    print("\\nWhen querying tenant 'acme_corp', the coordinator only queries Shard [", get_shard("acme_corp", num_shards), "]!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 43: Custom Document Routing ==="
python3 phases/43-document-routing/code/43_document_routing.py
"""),

        (44, "Distributed Search",
         "Distributed search is scatter-gather: the coordinator broadcasts to every shard, gathers top hits, and merges the global result.",
         """# Lesson 44.1: Distributed Search

## Motto
"Distributed search is scatter-gather: the coordinator broadcasts to every shard, gathers top hits, and merges the global result."

## Problem
When an index is split across 50 shards on 20 servers, how does a client obtain a globally sorted top-10 result list without transferring all documents across the network?

## Prediction
What happens if one shard out of 50 is slow or unresponsive during a scatter-gather search?

## Why this matters
Distributed search coordination introduces network latency, serialization overhead, and tail-latency sensitivity (the slow-shard problem).

## First principles
Scatter-Gather Protocol:
1. **Scatter:** Coordinating node sends lightweight query payload to one copy (primary or replica) of every shard in the index.
2. **Local Execution:** Each shard executes the query locally against its Lucene segments, computing local BM25 scores.
3. **Local Top-$K$:** Each shard returns its top $K$ candidate document IDs + scores.
4. **Gather & Merge:** Coordinating node priority-queue merges all shard results to determine the true global top $K$ winners.
5. **Fetch:** Coordinator requests `_source` only for winning IDs.

## Mental model
```text
                     CLIENT
                       │ GET /search?size=10
                       ▼
               COORDINATING NODE
             /         │         \
      Scatter          Scatter    Scatter
           ▼           ▼           ▼
       Shard 0      Shard 1     Shard 2
       (Top 10)     (Top 10)    (Top 10)
           \           │           /
        Gather       Gather      Gather
             \         │         /
               COORDINATING NODE
          Priority Queue: Merge 30 items
          ──► Select Global Top 10
                       │
                       ▼
                     CLIENT
```

## Build it
See `code/scatter_gather_sim.py` simulating multi-shard query coordination and merging in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/44-distributed-search/experiments/run_experiment.sh
```

## Inspect it
Observe shard execution metadata in the search response header:
```json
"_shards": {
  "total": 3,
  "successful": 3,
  "skipped": 0,
  "failed": 0
}
```

## Measure it
Measure search latency as shard count increases from 1 to 20 for the exact same dataset size.

## Break it
Simulate a slow shard by injecting latency on one node; observe how total request latency is bounded by the slowest shard.

## Recover it
Inspect `_cat/thread_pool/search` and optimize shard allocations.

## Modify it
Pass `preference=_local` or `preference=_shards:0,1` to target specific shard subsets.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is distributed search latency dictated by the slowest participating shard?
2. What is the fan-out network cost when an index has 100 primary shards?

## Guarantees
* The coordinator produces an accurately merged top-$K$ result across all participating shards.

## Non-guarantees
* Having more shards does NOT automatically decrease search latency.

## When to use this
* Standard distributed search across multi-shard indices.

## When not to use this
* When oversharding creates hundreds of tiny shards with near-zero data.

## What comes next
In Phase 45, we examine the mechanics of the Query-Then-Fetch protocol.
""",
"""#!/usr/bin/env python3
import heapq

def simulate_shard_search(shard_id, docs, query, top_k=5):
    # Local shard search
    candidates = []
    for doc_id, text in docs.items():
        if query in text:
            # Score simulation
            score = round(len(text) * 0.1 + (doc_id % 7) * 0.5, 2)
            candidates.append((score, doc_id, shard_id))
    candidates.sort(reverse=True)
    return candidates[:top_k]

def coordinate_scatter_gather(shards_data, query, top_k=5):
    # 1. Scatter to all shards
    gathered_candidates = []
    for s_id, docs in shards_data.items():
        shard_top = simulate_shard_search(s_id, docs, query, top_k)
        gathered_candidates.extend(shard_top)

    # 2. Global priority queue merge
    global_top = heapq.nlargest(top_k, gathered_candidates, key=lambda x: x[0])
    return global_top

if __name__ == "__main__":
    shards = {
        0: {1: "distributed search engine", 2: "kafka log engine"},
        1: {3: "search engine indexing", 4: "redis memory cache"},
        2: {5: "search relevance engine", 6: "postgres sql database"}
    }
    top_results = coordinate_scatter_gather(shards, "engine", top_k=3)
    print("Coordinating Node - Global Merged Top 3 Results:")
    for score, doc_id, shard_id in top_results:
        print(f"  Doc [{doc_id}] from Shard [{shard_id}] - Score: {score}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 44: Distributed Scatter-Gather Search ==="
python3 phases/44-distributed-search/code/44_distributed_search.py
"""),

        (45, "Query Then Fetch",
         "Query-Then-Fetch avoids transferring gigabytes of document bodies across nodes during ranking.",
         """# Lesson 45.1: Query Then Fetch

## Motto
"Query-Then-Fetch avoids transferring gigabytes of document bodies across nodes during ranking."

## Problem
If an index has 10 shards and you search for `size: 10`, what if each shard returned the full 500-KB `_source` JSON document for its top 10 candidates? 100 full documents (50 MB) would travel across the internal cluster network, only for the coordinator to discard 90 of them!

## Prediction
Why does Elasticsearch execute search in two separate roundtrips (Query phase, then Fetch phase) rather than one combined request?

## Why this matters
**Query-Then-Fetch** is the default search execution type in Elasticsearch. It separates relevance scoring from document retrieval.

## First principles
* **Phase 1 (Query Phase):**
  * Coordinator broadcasts query to all shards.
  * Shards return ONLY `(doc_id, score, sort_values)`.
  * Tiny network payload: a few bytes per candidate!
* **Merge:** Coordinator sorts candidate scores to identify the exact $K$ winning documents.
* **Phase 2 (Fetch Phase):**
  * Coordinator contacts only the specific shards hosting the winning $K$ documents.
  * Requests the full `_source`, stored fields, and highlights for those exact IDs.

## Mental model
```text
Roundtrip 1 (Query Phase):
  Coordinator ──► Shards: "Give me your top 10 IDs and BM25 scores."
  Shards ──────► Coordinator: Returns lightweight ID list: [(42, 3.8), (91, 2.9)...]

Roundtrip 2 (Fetch Phase):
  Coordinator ──► Shard 2: "Give me the full _source for Doc 42."
  Shard 2 ─────► Coordinator: Returns JSON body.
```

## Build it
See `code/query_then_fetch_sim.py` demonstrating network byte savings in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/45-query-then-fetch/experiments/run_experiment.sh
```

## Inspect it
Trace search phases using the `_profile` API:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "profile": true,
  "query": { "match": { "title": "keyboard" } }
}'
```

## Measure it
Compare total network bytes transferred under Query-Then-Fetch vs an eager full-document fetch.

## Break it
Request `from: 10000, size: 10000` (deep pagination): each shard must score and send 20,000 IDs to the coordinator, exhausting coordinator heap memory.

## Recover it
Enforce `index.max_result_window: 10000` (default safety limit) and migrate deep paging to `search_after`.

## Modify it
Use `stored_fields` or `docvalue_fields` during the fetch phase to retrieve specific attributes without decompressing `_source`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Query-Then-Fetch require two network roundtrips between coordinator and data nodes?
2. What happens during the Fetch phase if one of the winning documents was deleted between the Query and Fetch phases?

## Guarantees
* Maximizes network efficiency by transferring full document payloads only for winning hits.

## Non-guarantees
* Does not eliminate deep pagination sorting overhead (since all candidate IDs up to `from + size` must be collected).

## When to use this
* Default distributed search across all Elasticsearch indices.

## When not to use this
* Single-shard indices (Elasticsearch automatically optimizes single-shard queries).

## What comes next
In Phase 46, we analyze Shard Count sizing and benchmarking.
""",
"""#!/usr/bin/env python3

def simulate_search_phases(num_shards=5, page_size=10, doc_size_kb=50):
    # Eager approach: each shard returns full docs
    eager_bytes_kb = num_shards * page_size * doc_size_kb

    # Query-Then-Fetch:
    # Query phase: each shard returns (id, score) ≈ 16 bytes
    query_phase_bytes = (num_shards * page_size * 16) / 1024
    # Fetch phase: only page_size winning docs fetched
    fetch_phase_bytes = page_size * doc_size_kb
    qtf_total_kb = query_phase_bytes + fetch_phase_bytes

    return eager_bytes_kb, qtf_total_kb

if __name__ == "__main__":
    eager, qtf = simulate_search_phases(num_shards=10, page_size=10, doc_size_kb=100)
    print("Network Payload Comparison (10 Shards, size=10, 100KB doc body):")
    print(f"  Naive Eager Fetch:     {eager:8.1f} KB transferred across cluster")
    print(f"  Query-Then-Fetch:      {qtf:8.1f} KB transferred across cluster")
    print(f"  Bandwidth saved:       {((eager - qtf) / eager) * 100:.1f}%!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 45: Query-Then-Fetch Protocol ==="
python3 phases/45-query-then-fetch/code/45_query_then_fetch.py
"""),

        (46, "Shard Count",
         "More shards is not always faster: shard count is a capacity decision, not a performance dial.",
         """# Lesson 46.1: Shard Count

## Motto
"More shards is not always faster: shard count is a capacity decision, not a performance dial."

## Problem
A team creates an index for 1 GB of data and configures 20 primary shards, assuming "more shards = more parallel threads = 20x faster search". In reality, queries become 3x slower and cluster metadata bloats!

## Prediction
Will a 50MB index search faster with 1 primary shard or with 10 primary shards?

## Why this matters
Sharding introduces overhead: thread context switches, network serialization, memory per segment, and coordinator reduce time.

## First principles
Rules of Thumb for Shard Sizing:
* **Recommended Shard Size:** 10 GB to 50 GB per shard for standard search; up to 50 GB for time-series logs.
* If your entire dataset is 2 GB, it belongs in **1 primary shard**!
* Each shard consumes JVM heap memory for segment dictionaries and open file descriptors.

## Mental model
```text
50 MB Dataset in 1 Shard:
  Coordinator ──► 1 Shard ──► Return Hits. (Zero Network Fan-Out, ~2ms)

50 MB Dataset in 20 Shards:
  Coordinator ──► 20 Shards ──► 20 TCP roundtrips ──► Coordinator merges 20 queues. (~15ms!)
```

## Build it
See `code/shard_count_bench.py` simulating fan-out latency scaling in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/46-shard-count/experiments/run_experiment.sh
```

## Inspect it
Compare search latency between an index with 1 shard vs 10 shards on identical data:
```bash
curl -X PUT http://localhost:9200/idx_1shard -H "Content-Type: application/json" -d '{"settings": {"number_of_shards": 1, "number_of_replicas": 0}}'
curl -X PUT http://localhost:9200/idx_10shards -H "Content-Type: application/json" -d '{"settings": {"number_of_shards": 10, "number_of_replicas": 0}}'
```

## Measure it
Benchmark query latency on both indices and observe that 1 shard outperforms 10 shards on small data.

## Break it
Create 1,000 tiny shards in a test cluster and observe cluster state sync lag and JVM heap consumption.

## Recover it
Use `_shrink` API or Reindex to consolidate into fewer, properly sized shards.

## Modify it
Calculate target shard count based on expected annual data volume.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an index with 20 primary shards perform worse on small datasets than an index with 1 shard?
2. What is the generally recommended shard size range in production?

## Guarantees
* A single shard eliminates all distributed scatter-gather coordination overhead.

## Non-guarantees
* A single shard cannot scale beyond the physical storage limit of one server.

## When to use this
* Capacity planning and initial index architecture.

## When not to use this
* Blindly accepting defaults without calculating data volume.

## What comes next
In Phase 47, we examine the production disaster of Oversharding.
""",
"""#!/usr/bin/env python3
import time

def simulate_fanout(num_shards, base_shard_latency_ms=1.5, per_shard_network_overhead_ms=0.3):
    # Simulated coordinator wait: max of shard latencies + merge cost
    import random
    random.seed(42)
    shard_times = [base_shard_latency_ms + random.uniform(0.1, 0.8) for _ in range(num_shards)]
    coordination_merge_time = num_shards * per_shard_network_overhead_ms
    total_time = max(shard_times) + coordination_merge_time
    return total_time

if __name__ == "__main__":
    print("Simulated Search Latency for 100MB Dataset across varying Shard Counts:\\n")
    for s_count in [1, 2, 5, 10, 20, 50]:
        lat = simulate_fanout(s_count)
        print(f"  {s_count:2d} Primary Shards: {lat:6.2f} ms")
    print("\\nNotice how coordination fan-out increases latency on small datasets!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 46: Shard Count Benchmarking ==="
python3 phases/46-shard-count/code/46_shard_count.py
"""),

        (47, "Oversharding",
         "Thousands of tiny shards cause death by a thousand cuts: heap exhaustion, thread contention, and slow recovery.",
         """# Lesson 47.1: Oversharding

## Motto
"Thousands of tiny shards cause death by a thousand cuts: heap exhaustion, thread contention, and slow recovery."

## Problem
A company creates daily indices with 5 primary shards and 1 replica for each microservice. After 2 years, the cluster hosts 15,000 shards across only 3 nodes (averaging 5,000 shards per node!). The cluster master freezes, searches time out, and nodes crash with OutOfMemory errors.

## Prediction
Why does each Lucene shard consume JVM heap memory even when it receives zero search and write traffic?

## Why this matters
Oversharding is the #1 cause of unprovoked Elasticsearch cluster instability.

## First principles
The Cost of a Shard:
1. **JVM Heap:** Each shard holds open Lucene segment metadata, FST term dictionaries, and doc values readers in memory (approx 10MB to 50MB of heap per shard, even if empty!).
2. **File Descriptors:** Each shard holds dozens of open file handles on disk.
3. **Master Coordination:** The active master node must broadcast the status of every single shard in the cluster state. A 100MB cluster state payload causes network partitions and master election loops.
4. **Thread Contention:** A search across 2,000 shards overwhelms search thread pool queues.

## Mental model
```text
Healthy Cluster:
  30 Shards (30GB each) ──► Low Heap, Low Thread Contention, Instant Recovery

Oversharded Cluster:
  3,000 Shards (30MB each) ──► 3,000 Lucene directories in memory ──► CLUSTER COLLAPSE!
```

## Build it
See `code/oversharding_calculator.py` estimating heap memory consumption per shard count in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/47-oversharding/experiments/run_experiment.sh
```

## Inspect it
Check your cluster's total shard count per node:
```bash
curl -s "http://localhost:9200/_cat/nodes?v&h=name,node.role,shards,heap.percent"
```

## Measure it
Observe the guideline: maintain **under 20 shards per GB of JVM heap** on any data node.

## Break it
Inspect cluster health when shard limits are approached (`cluster.max_shards_per_node`, default 1,000 in modern ES).

## Recover it
1. Delete obsolete indices.
2. Shrink indices via `_shrink`.
3. Consolidate daily indices into monthly indices via `_reindex`.
4. Implement Index Lifecycle Management (ILM, Phase 66).

## Modify it
Calculate optimal shard allocation for a 500GB logging cluster.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an empty shard consume JVM heap memory?
2. What is the recommended maximum ratio of shards to JVM heap gigabytes?

## Guarantees
* Limiting shard count preserves master node responsiveness and keeps cluster state compact.

## Non-guarantees
* Shard limits alone cannot prevent OOM if individual aggregations exceed heap memory.

## When to use this
* Cluster health auditing, capacity reviews, and architectural sizing.

## When not to use this
* Ignoring shard counts until the cluster turns red.

## What comes next
In Phase 48, we study Replicas and their role in High Availability.
""",
"""#!/usr/bin/env python3

def calculate_shard_overhead(num_shards, heap_per_shard_mb=15):
    total_heap_mb = num_shards * heap_per_shard_mb
    total_heap_gb = total_heap_mb / 1024.0
    return total_heap_mb, total_heap_gb

if __name__ == "__main__":
    scenarios = [50, 500, 2000, 5000, 10000]
    print(f"{'Shard Count':15s} | {'Static Heap Consumed':25s} | {'Node Heap Impact (31GB Max)'}")
    print("-" * 75)
    for sc in scenarios:
        mb, gb = calculate_shard_overhead(sc)
        pct = (gb / 31.0) * 100
        print(f"{sc:15d} | {mb:6d} MB ({gb:5.1f} GB)          | {pct:5.1f}% of 31GB heap")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 47: Oversharding Analysis ==="
python3 phases/47-oversharding/code/47_oversharding.py
"""),

        (48, "Replicas",
         "A replica is an exact copy of a primary shard: it provides zero-downtime failover and scales read throughput.",
         """# Lesson 48.1: Replicas

## Motto
"A replica is an exact copy of a primary shard: it provides zero-downtime failover and scales read throughput."

## Problem
You have an index with 1 primary shard on Node A. Node A suffers a hardware failure and loses power. Your index is immediately 100% offline and all user searches fail with HTTP 503 errors.

## Prediction
If you configure `number_of_replicas: 1` on a 2-node cluster and Node A dies, can Node B continue serving search queries without data loss?

## Why this matters
Replicas provide High Availability (HA) and read scaling. Understanding the primary-replica lifecycle is crucial for distributed reliability.

## First principles
Two Fundamental Roles of Replicas:
1. **High Availability (Failover):** If the node holding the primary shard dies, Elasticsearch automatically promotes a replica shard to primary in milliseconds. Zero downtime, zero data loss.
2. **Read Scaling:** Replicas are fully functional, independent Lucene search indices. Search queries are load-balanced round-robin across primaries and replicas!

## Mental model
```text
Write Path:
  Client ──► Primary Shard (Node 1) ──► Replicates to Replica Shard (Node 2)

Read Path:
  Query 1 ──► Primary Shard (Node 1)
  Query 2 ──► Replica Shard (Node 2)  (Doubles Read Query Capacity!)
```

## Build it
See `code/replica_failover_sim.py` demonstrating primary promotion and read load balancing in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/48-replicas/experiments/run_experiment.sh
```

## Inspect it
Dynamically change replica count on a live index:
```bash
curl -X PUT http://localhost:9200/sharded_index/_settings -H "Content-Type: application/json" -d '{
  "index": { "number_of_replicas": 1 }
}'
```

## Measure it
Inspect shard allocation with `_cat/shards`: primary (`p`) vs replica (`r`).

## Break it
Set `number_of_replicas: 1` on a single-node cluster: observe cluster status turns **YELLOW** because Elasticsearch refuses to place a replica on the same physical node as the primary!

## Recover it
Either start a second node (via `make cluster-up`) or set `number_of_replicas: 0`.

## Modify it
Benchmark read query QPS with 0 replicas vs 2 replicas on a multi-node cluster.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch refuse to allocate a replica shard on the same physical node as its primary shard?
2. How do replicas double read throughput without doubling write throughput?

## Guarantees
* Replicas provide transparent failover if a primary shard node fails.

## Non-guarantees
* Replicas do NOT protect against user error (e.g. `DELETE /index` deletes primaries and replicas simultaneously!). Replicas != Backups!

## When to use this
* Every production index (minimum `number_of_replicas: 1`).

## When not to use this
* Temporary local development or initial bulk migrations where write speed is priority and replicas will be enabled later.

## What comes next
In Phase 49, we perform live Node Failure and observe automatic failover.
""",
"""#!/usr/bin/env python3

class ClusterReplicaSim:
    def __init__(self):
        self.nodes = {
            "node_1": {"role": "primary", "alive": True, "docs": [1, 2, 3]},
            "node_2": {"role": "replica", "alive": True, "docs": [1, 2, 3]}
        }

    def search(self, query):
        # Round-robin across alive copies
        alive_nodes = [name for name, data in self.nodes.items() if data["alive"]]
        if not alive_nodes:
            raise RuntimeError("HTTP 503: Cluster Red - All shard copies offline!")
        chosen = alive_nodes[0]
        return f"Served from {chosen} ({self.nodes[chosen]['role']})"

    def kill_node(self, node_name):
        print(f"\\n[CRASH] Killing {node_name}...")
        self.nodes[node_name]["alive"] = False
        # Master node failover detection
        if self.nodes[node_name]["role"] == "primary":
            for n, d in self.nodes.items():
                if d["alive"] and d["role"] == "replica":
                    d["role"] = "primary"
                    print(f"  [PROMOTION] Promoted {n} to PRIMARY shard!")

if __name__ == "__main__":
    cluster = ClusterReplicaSim()
    print("Initial state:", cluster.search("query 1"))
    cluster.kill_node("node_1")
    print("State after node_1 crash:", cluster.search("query 2"))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 48: Replicas & High Availability ==="
python3 phases/48-replicas/code/48_replicas.py
"""),

        (49, "Node Failure",
         "Controlled failure testing: kill the node holding a primary shard and observe real-time failover and shard recovery.",
         """# Lesson 49.1: Node Failure

## Motto
"Controlled failure testing: kill the node holding a primary shard and observe real-time failover and shard recovery."

## Problem
Engineers assume high-availability works because it is written in documentation. In production, when a node drops off the network, unexpected timeouts occur because teams have never observed live failover.

## Prediction
If a 3-node cluster loses Node 1 holding Primary Shard 0:
1. What does cluster health become?
2. How many seconds does failover take?
3. Do search queries fail during promotion?

## Why this matters
Master node heartbeats, replica promotion, and peer recovery are the core distributed resilience mechanisms of Elasticsearch.

## First principles
Failover Sequence:
1. Master node detects missing heartbeats from Node 1 (default 10s ping timeout).
2. Master updates cluster state: marks Node 1 dead.
3. Master checks for active replica shards of missing primaries.
4. Promotes Replica Shard 0 on Node 2 to **Primary**.
5. Cluster health transitions from **GREEN $\to$ YELLOW** (all primaries active, but missing a replica).
6. Master allocates a new unassigned replica on Node 3 and begins **Peer Recovery** (copying Lucene segments over network).
7. Once sync finishes, cluster transitions back to **GREEN**!

## Mental model
```text
T0: Healthy (Green)
  Node 1: Primary 0  |  Node 2: Replica 0  |  Node 3: Master

T1: Kill Node 1!
  Node 1: [DEAD]     |  Node 2: Replica 0  |  Node 3: Master (Detects dead node)

T2: Failover (Yellow)
  Node 1: [DEAD]     |  Node 2: PRIMARY 0  |  Node 3: Starts peer recovery to Node 3

T3: Recovered (Green)
  Node 1: [DEAD]     |  Node 2: PRIMARY 0  |  Node 3: REPLICA 0 (Data replicated!)
```

## Build it
See `code/node_failure_monitor.py` polling cluster state changes during failure.

## Use Elasticsearch
Run the experiment against the 3-node cluster lab (`docker-compose.cluster.yml`):
```bash
./phases/49-node-failure/experiments/run_experiment.sh
```

## Inspect it
Observe active cluster nodes before and after:
```bash
curl -s "http://localhost:9200/_cat/nodes?v"
curl -s "http://localhost:9200/_cat/shards?v"
```

## Measure it
Measure time elapsed from container termination (`docker stop es-cluster-02`) to replica promotion.

## Break it
Kill the active master node (`es01`) and observe how the remaining two nodes elect a new master via Raft-based consensus without data loss.

## Recover it
Restart the stopped container (`docker start es-cluster-02`) and watch Elasticsearch re-balance and re-assign shards.

## Modify it
Inspect cluster health recovery speed with `_cat/recovery`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does cluster health turn YELLOW and not RED when a node hosting a primary shard dies (assuming replicas exist)?
2. How does peer recovery avoid re-copying existing matching Lucene segments? (Engine uses sequence numbers and translog replay).

## Guarantees
* As long as at least one primary or replica shard exists, data remains available for search.

## Non-guarantees
* If a node dies while hosting an un-replicated primary (`number_of_replicas: 0`), that shard's data is lost and the cluster turns RED.

## When to use this
* Disaster recovery validation and chaos engineering drills.

## When not to use this
* Do not terminate nodes in production during active unthrottled reindexing.

## What comes next
In Phase 50, we define and live-trigger Cluster Health states: Green, Yellow, and Red.
""",
"""#!/usr/bin/env python3
import time

def simulate_cluster_heartbeat(nodes_alive):
    primary_active = "node_1" in nodes_alive or "node_2" in nodes_alive
    replica_active = "node_1" in nodes_alive and "node_2" in nodes_alive

    if primary_active and replica_active:
        return "GREEN", "All primaries and replicas active."
    elif primary_active and not replica_active:
        return "YELLOW", "Primaries active; replica missing (redundancy degraded)."
    else:
        return "RED", "Primary shard offline! Data loss / search unavailability."

if __name__ == "__main__":
    states = [
        {"desc": "Normal Operation", "nodes": ["node_1", "node_2", "node_3"]},
        {"desc": "Node 1 Crashes (Primary lost, promoted replica)", "nodes": ["node_2", "node_3"]},
        {"desc": "Node 2 Crashes (All copies lost)", "nodes": ["node_3"]}
    ]
    for s in states:
        color, explanation = simulate_cluster_heartbeat(s["nodes"])
        print(f"Scenario: {s['desc']:50s} -> Health: [{color:6s}] - {explanation}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 49: Node Failure & Promotion Simulation ==="
python3 phases/49-node-failure/code/49_node_failure.py
"""),

        (50, "Cluster Health",
         "Green means all shards assigned; Yellow means data is safe but redundancy is compromised; Red means data is missing.",
         """# Lesson 50.1: Cluster Health

## Motto
"Green means all shards assigned; Yellow means data is safe but redundancy is compromised; Red means data is missing."

## Problem
On-call engineers often wake up to an alert: *"Cluster health is YELLOW"*. Panicking, they restart random nodes, accidentally turning a temporary yellow state into a catastrophic RED data outage.

## Prediction
Can user search queries still execute and return valid results when cluster health is YELLOW? What about when RED?

## Why this matters
Cluster health is the primary metric reported by Elasticsearch. Knowing exactly what each color guarantees prevents dangerous operational missteps.

## First principles
The Three Health States:
* **GREEN:** All primary shards AND all replica shards are allocated to active nodes. 100% capacity and full redundancy.
* **YELLOW:** All primary shards are active, but one or more replica shards are unassigned. **All data is 100% searchable and writable.** Redundancy is reduced: if the remaining node dies, data loss will occur.
* **RED:** At least one primary shard is unassigned and offline. **Data is missing.** Searches hitting that shard will fail or return partial hits!

## Mental model
```text
┌──────────┐
│  GREEN   │ ──► All Primaries Assigned + All Replicas Assigned. Full HA.
└──────────┘
┌──────────┐
│  YELLOW  │ ──► All Primaries Assigned. NO DATA LOST! (Missing some replicas).
└──────────┘
┌──────────┐
│   RED    │ ──► At least one Primary Shard OFFLINE! Data is currently missing!
└──────────┘
```

## Build it
See `code/cluster_health_state_machine.py` modeling health transitions in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/50-cluster-health/experiments/run_experiment.sh
```

## Inspect it
Check cluster health:
```bash
curl -s http://localhost:9200/_cluster/health?pretty
```

## Measure it
Inspect shard counts in `_cluster/health`:
* `active_primary_shards`
* `active_shards`
* `unassigned_shards`

## Break it
Intentionally turn the cluster YELLOW by setting `number_of_replicas: 1` in our single-node lab:
```bash
curl -X PUT http://localhost:9200/yellow_demo -H "Content-Type: application/json" -d '{"settings": {"number_of_replicas": 1}}'
curl -s http://localhost:9200/_cluster/health?pretty | grep "status"
```

## Recover it
Turn the cluster back to GREEN by setting replicas to 0:
```bash
curl -X PUT http://localhost:9200/yellow_demo/_settings -H "Content-Type: application/json" -d '{"index": {"number_of_replicas": 0}}'
curl -s http://localhost:9200/_cluster/health?pretty | grep "status"
```

## Modify it
Wait for a specific health status in automation scripts: `GET /_cluster/health?wait_for_status=green&timeout=30s`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an unassigned replica shard make cluster health YELLOW rather than RED?
2. If cluster health is RED, does Elasticsearch reject all search queries, or does it return partial hits?

## Guarantees
* YELLOW cluster health guarantees zero data loss and full query availability at the current moment.

## Non-guarantees
* YELLOW does not guarantee safety if another node fails.

## When to use this
* Every automated health check, deployment pipeline, and alerting monitor.

## When not to use this
* As the sole metric for performance (a green cluster can still suffer 5-second search latency).

## What comes next
In Phase 51, we investigate Shard Allocation and diagnostic deciders.
""",
"""#!/usr/bin/env python3

def evaluate_cluster_health(shards):
    # shards: list of dicts: {"shard": id, "type": "primary"|"replica", "assigned": bool}
    primaries = [s for s in shards if s["type"] == "primary"]
    replicas = [s for s in shards if s["type"] == "replica"]

    if not all(p["assigned"] for p in primaries):
        return "RED", "One or more primary shards are unassigned!"
    if not all(r["assigned"] for r in replicas):
        return "YELLOW", "All primaries active, but some replicas are unassigned."
    return "GREEN", "All primary and replica shards successfully assigned."

if __name__ == "__main__":
    test_shards = [
        {"shard": 0, "type": "primary", "assigned": True},
        {"shard": 0, "type": "replica", "assigned": False}
    ]
    status, reason = evaluate_cluster_health(test_shards)
    print(f"Cluster Status: [{status}]")
    print(f"Reason: {reason}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 50: Cluster Health Transitions ==="
python3 phases/50-cluster-health/code/50_cluster_health.py
"""),

        (51, "Shard Allocation",
         "The cluster allocator evaluates deciders: disk thresholds, node filters, shard limits, and replica anti-affinity.",
         """# Lesson 51.1: Shard Allocation

## Motto
"The cluster allocator evaluates deciders: disk thresholds, node filters, shard limits, and replica anti-affinity."

## Problem
A replica shard remains persistently `UNASSIGNED`. Why did the master node refuse to place it? Guessing the cause leads to fruitless node restarts.

## Prediction
Can Elasticsearch tell you the exact algorithmic reason why a specific shard cannot be placed on any node in the cluster?

## Why this matters
The `_cluster/allocation/explain` API is the single most powerful diagnostic tool for fixing unassigned shards and cluster health issues.

## First principles
The Allocation Process & Deciders:
1. **`same_shard` decider:** Rejects allocating primary and replica of the same shard on the same physical node.
2. **`disk_threshold` decider:** Rejects allocation if node disk usage exceeds low watermark (85%).
3. **`shards_limit` decider:** Rejects if node already holds max shards per node.
4. **`awareness` decider:** Distributes shards across availability zones or racks.

## Mental model
```text
Allocator: "Can I put Replica Shard 0 on Node A?"
  ├── Decider 'same_shard': NO (Node A already has Primary Shard 0!)
Allocator: "Can I put Replica Shard 0 on Node B?"
  ├── Decider 'same_shard': YES
  ├── Decider 'disk_threshold': NO (Node B is at 89% disk usage!)
Result: Shard remains UNASSIGNED.
```

## Build it
See `code/allocation_decider_sim.py` simulating allocation rules in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/51-shard-allocation/experiments/run_experiment.sh
```

## Inspect it
Run `_cluster/allocation/explain` to diagnose why an unassigned shard cannot allocate:
```bash
curl -X POST http://localhost:9200/_cluster/allocation/explain?pretty -H "Content-Type: application/json" -d '{
  "index": "yellow_demo",
  "shard": 0,
  "primary": false
}'
```
Read the exact `decider` output in the JSON response!

## Measure it
Inspect shard movement events using `_cat/shards?v&s=state`.

## Break it
Set `cluster.routing.allocation.enable: "none"` and create an index. All shards remain stuck in unassigned state!

## Recover it
Reset allocation: `PUT /_cluster/settings {"transient": {"cluster.routing.allocation.enable": "all"}}`.

## Modify it
Configure allocation filtering to route indices to specific hardware tiers (e.g. `index.routing.allocation.include._tier: "data_hot"`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What does the `same_shard` allocation decider enforce?
2. How does `_cluster/allocation/explain` help on-call engineers resolve unassigned shards?

## Guarantees
* Shard allocation deciders prevent data loss and prevent overloading stressed nodes.

## Non-guarantees
* The allocator cannot place shards if hardware resources (disk/nodes) are physically insufficient.

## When to use this
* Investigating any yellow or red cluster status.

## When not to use this
* Routine operations when cluster health is green.

## What comes next
In Phase 52, we study Cluster State: the coordinated metadata of the cluster.
""",
"""#!/usr/bin/env python3

def evaluate_allocation(node, shard):
    # Rule 1: Cannot place primary and replica on same node
    if shard["id"] in node["existing_shards"]:
        return False, "same_shard: node already hosts a copy of this shard"
    # Rule 2: Disk watermark
    if node["disk_usage_pct"] >= 85:
        return False, f"disk_threshold: node disk usage ({node['disk_usage_pct']}%) exceeds low watermark 85%"
    return True, "allocation allowed"

if __name__ == "__main__":
    node_a = {"name": "node-01", "disk_usage_pct": 50, "existing_shards": [0]}
    node_b = {"name": "node-02", "disk_usage_pct": 89, "existing_shards": []}
    shard = {"id": 0, "type": "replica"}

    print("Evaluating Shard Allocation for Replica Shard 0:")
    for n in [node_a, node_b]:
        allowed, reason = evaluate_allocation(n, shard)
        print(f"  Target: {n['name']} -> Allowed? {allowed} (Reason: {reason})")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 51: Shard Allocation & Diagnostics ==="
python3 phases/51-shard-allocation/code/51_shard_allocation.py
"""),

        (52, "Cluster State",
         "Cluster state is the single source of truth: master consensus distributes mappings, indices, and shard routing tables.",
         """# Lesson 52.1: Cluster State

## Motto
"Cluster state is the single source of truth: master consensus distributes mappings, indices, and shard routing tables."

## Problem
In a 20-node cluster, how does every node know which shard lives on which IP address, what data types exist in mappings, and which indices are open? If nodes have conflicting metadata, writes and searches go to the wrong servers.

## Prediction
What happens to cluster stability if cluster state metadata grows from 2 MB to 200 MB?

## Why this matters
Cluster State is coordinated by the elected **Master Node**. Understanding its size and broadcast frequency explains why mapping explosions and oversharding destabilize clusters.

## First principles
Cluster State Contents:
* Active cluster nodes list
* Indices metadata (settings, mappings)
* Shard routing tables (which shard is on which node)
* Index templates and ILM policies
Every time an index is created, mapping updated, or shard relocated, the Master updates the cluster state and broadcasts a diff to all nodes.

## Mental model
```text
ELECTED MASTER NODE
┌────────────────────────────────────────────────────────┐
│ Cluster State (Metadata, Routing Tables, Mappings)     │
└───────────────────────────┬────────────────────────────┘
                            │ Broadcast Diffs via Transport TCP (:9300)
             ┌──────────────┴──────────────┐
             ▼                             ▼
      DATA NODE 1                    DATA NODE 2
  (Keeps local copy)             (Keeps local copy)
```

## Build it
See `code/cluster_state_sim.py` simulating metadata broadcast in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/52-cluster-state/experiments/run_experiment.sh
```

## Inspect it
Inspect cluster state summary (exclude huge mappings to keep output readable):
```bash
curl -s "http://localhost:9200/_cluster/state/version,master_node,nodes?pretty"
```

## Measure it
Inspect the cluster state size and version number:
```bash
curl -s "http://localhost:9200/_cluster/stats?pretty" | grep -A 5 "cluster_state"
```

## Break it
Generate hundreds of indices with thousands of dynamic fields rapidly. Observe master node CPU spike as it attempts to serialize and broadcast huge metadata updates.

## Recover it
Limit dynamic mapping and consolidate indices.

## Modify it
Inspect master node tasks: `curl -s http://localhost:9200/_cluster/pending_tasks?pretty`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does every node in an Elasticsearch cluster maintain a copy of the cluster state?
2. What role does the active master node play in updating cluster state?

## Guarantees
* The master node guarantees linearizable cluster state updates across nodes.

## Non-guarantees
* Cluster state does not contain document bodies; only metadata.

## When to use this
* Auditing cluster health, metadata size, and master node performance.

## When not to use this
* Querying `GET _cluster/state` on large production clusters without filtering specific components (can return hundreds of megabytes of JSON).

## What comes next
In Phase 53, we investigate the deadly operational crisis: Mapping Explosion.
""",
"""#!/usr/bin/env python3

class ClusterMetadataCoordinator:
    def __init__(self):
        self.version = 1
        self.nodes = ["node-1", "node-2", "node-3"]
        self.indices = {}

    def update_mapping(self, index_name, new_field, field_type):
        self.version += 1
        self.indices.setdefault(index_name, {})[new_field] = field_type
        # Broadcast diff to all nodes
        diff = f"v{self.version}: Added {new_field}:{field_type} to {index_name}"
        return diff

if __name__ == "__main__":
    master = ClusterMetadataCoordinator()
    print("Master Node initialized. Cluster State Version:", master.version)
    diff1 = master.update_mapping("users", "email", "keyword")
    print("Broadcast:", diff1)
    diff2 = master.update_mapping("users", "age", "integer")
    print("Broadcast:", diff2)
    print("Current State Version:", master.version)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 52: Cluster State Metadata ==="
python3 phases/52-cluster-state/code/52_cluster_state.py
"""),

        (53, "Mapping Explosion",
         "A mapping explosion occurs when arbitrary user keys become schema fields, ballooning cluster state and crashing the master node.",
         """# Lesson 53.1: Mapping Explosion

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
""",
"""#!/usr/bin/env python3

def bad_modeling_dynamic_fields(user_ids):
    # Generates unique field per user
    fields = set()
    for uid in user_ids:
        fields.add(f"user_{uid}")
    return fields

def good_modeling_array(user_ids):
    # Fixed schema: 1 field
    return {"users_active": len(user_ids)}

if __name__ == "__main__":
    simulated_users = list(range(5000))
    bad_fields = bad_modeling_dynamic_fields(simulated_users)
    print("Anti-Pattern (Dynamic Field per ID):")
    print(f"  Total fields created in mapping: {len(bad_fields)} fields! (Triggers Mapping Explosion)")

    print("\\nBest Practice (Fixed Array or Flattened):")
    print(f"  Total fields created in mapping: 1 field! (Stable)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 53: Mapping Explosion Prevention ==="
python3 phases/53-mapping-explosion/code/53_mapping_explosion.py
"""),

        (54, "High Cardinality",
         "High cardinality fields have millions of unique values: aggregating on them strains doc values and coordinator memory.",
         """# Lesson 54.1: High Cardinality

## Motto
"High cardinality fields have millions of unique values: aggregating on them strains doc values and coordinator memory."

## Problem
A query requests a `terms` aggregation on `session_uuid` across 50 million web events:
`"aggs": { "all_sessions": { "terms": { "field": "session_uuid", "size": 100000 } } }`
The query takes 25 seconds, transfers 100MB of bucket metadata per shard, and exhausts coordinator memory.

## Prediction
Why is a `terms` aggregation on `country` (cardinality ~200) vastly faster than a `terms` aggregation on `user_uuid` (cardinality 10,000,000)?

## Why this matters
**Cardinality** (the number of distinct unique values in a field) dictates aggregation memory consumption and network transfer size across shards.

## First principles
* **Low Cardinality (e.g. status: 5 values):** Shards compute 5 bucket counts, coordinator merges 5 buckets. Instant.
* **High Cardinality (e.g. UUID: millions of values):** Shards must evaluate and track millions of distinct string values in doc values and priority queues.
* Coordinator must merge massive candidate lists from all shards.

## Mental model
```text
Low Cardinality (country: 3 values):
  Shard 0: [US: 100, UK: 50, CA: 30] ──► Coordinator merges 3 numbers!

High Cardinality (user_id: 1,000,000 unique values):
  Shard 0: 1,000,000 bucket objects in RAM ──► Massive coordination bottleneck!
```

## Build it
See `code/cardinality_impact_sim.py` demonstrating memory scaling with unique value counts in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/54-high-cardinality/experiments/run_experiment.sh
```

## Inspect it
Test `cardinality` aggregation (HyperLogLog++) vs `terms` aggregation on high-cardinality values:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "approx_count": { "cardinality": { "field": "category" } }
  }
}'
```

## Measure it
Compare aggregation latency as field cardinality increases from 10 to 100,000 unique items.

## Break it
Request `terms` aggregation with `size: 100000` on a high-cardinality field and observe query latency degrade.

## Recover it
1. Use `cardinality` aggregation instead of `terms` if only the distinct count is needed.
2. Filter before aggregating to reduce candidate document count.

## Modify it
Tune `shard_size` to balance accuracy vs coordination memory.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is computing the count of unique values with `cardinality` aggregation faster than running a `terms` aggregation?
2. What does `shard_size` control during high-cardinality terms aggregations?

## Guarantees
* HyperLogLog++ cardinality aggregation runs in constant bounded memory regardless of item count.

## Non-guarantees
* High-cardinality `terms` aggregations cannot bypass the memory cost of building thousands of buckets.

## When to use this
* Aggregation performance tuning and schema cardinality auditing.

## When not to use this
* Grouping by high-cardinality identifiers across millions of records.

## What comes next
In Phase 55, we examine Hot Shards: diagnosing uneven distributed load.
""",
"""#!/usr/bin/env python3
import time
import sys
from collections import defaultdict

def benchmark_cardinality_grouping(num_items, unique_values):
    data = [f"val_{i % unique_values}" for i in range(num_items)]
    t0 = time.perf_counter()
    counts = defaultdict(int)
    for v in data:
        counts[v] += 1
    elapsed = (time.perf_counter() - t0) * 1000
    memory_bytes = sys.getsizeof(counts)
    return elapsed, memory_bytes, len(counts)

if __name__ == "__main__":
    N = 200000
    print(f"Grouping {N} items by varying cardinality:\\n")
    for u in [5, 100, 5000, 50000]:
        ms, mem, buckets = benchmark_cardinality_grouping(N, u)
        print(f"  Unique Values: {u:6d} -> Buckets: {buckets:6d} | Time: {ms:6.2f} ms | Hash Map RAM: {mem:8d} bytes")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 54: High Cardinality Aggregations ==="
python3 phases/54-high-cardinality/code/54_high_cardinality.py
"""),

        (55, "Hot Shards",
         "A distributed cluster is only as fast as its most overloaded shard: key skew and bad routing create hot shards.",
         """# Lesson 55.1: Hot Shards

## Motto
"A distributed cluster is only as fast as its most overloaded shard: key skew and bad routing create hot shards."

## Problem
A 10-node cluster has 9 idle nodes at 5% CPU, while 1 single node is pinned at 100% CPU with search threads constantly timing out. Even though 90% of the cluster is idle, total application latency degrades.

## Prediction
What causes one specific shard or node to receive 10x more search or indexing traffic than peer shards?

## Why this matters
Distributed systems assume balanced load. A **Hot Shard** bottlenecks the entire cluster, negating the benefits of horizontal scaling.

## First principles
Causes of Hot Shards:
1. **Custom Routing Skew:** A single customer/tenant generates 80% of all writes and searches, overloading their designated shard.
2. **Monotonic Key Routing:** All recent time-series data hits the newest active shard.
3. **Uneven Shard Sizing:** One shard contains 100GB of data while others have 5GB.
4. **Heavy Wildcard or Aggregation Queries:** Repeatedly hitting the same specific shard.

## Mental model
```text
Balanced Cluster (Ideal):
  Node 1: [Shard 0] (10% CPU)  |  Node 2: [Shard 1] (10% CPU)  |  Node 3: [Shard 2] (10% CPU)

Hot Shard Bottleneck (Skew):
  Node 1: [Shard 0] (99% CPU - HOT!) ──► CLUSTER SEARCH THROTTLED!
  Node 2: [Shard 1] ( 2% CPU)
  Node 3: [Shard 2] ( 3% CPU)
```

## Build it
See `code/hot_shard_simulator.py` simulating skewed traffic distributions in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/55-hot-shards/experiments/run_experiment.sh
```

## Inspect it
Identify hot threads on cluster nodes:
```bash
curl -s http://localhost:9200/_nodes/hot_threads
```
Inspect CPU and indexing rate across shards:
```bash
curl -s "http://localhost:9200/_cat/shards?v&s=docs:desc"
```

## Measure it
Compare CPU utilization and queue depths across data nodes.

## Break it
Simulate hot shard traffic by sending thousands of writes with the same routing key to one node.

## Recover it
1. Use `index.routing_partition_size` to spread large tenants across multiple shards.
2. Re-route shards away from stressed nodes using `_cluster/reroute`.

## Modify it
Inspect thread pool write rejections on the hot node.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an idle node not automatically help a peer node suffering from a hot shard?
2. How does the `_nodes/hot_threads` API reveal CPU bottlenecks?

## Guarantees
* Elasticsearch provides diagnostic APIs (`hot_threads`, `_cat/shards`) to pinpoint unbalanced load.

## Non-guarantees
* Elasticsearch cannot magically balance traffic if the application data model is intrinsically skewed.

## When to use this
* Capacity troubleshooting, load balancing diagnosis, and multi-tenant performance tuning.

## When not to use this
* Perfectly uniform workloads where all nodes share equal load.

## What comes next
In Phase 56, we examine Search Caching mechanisms.
""",
"""#!/usr/bin/env python3
from collections import defaultdict
import random

def simulate_traffic(num_shards=5, total_requests=10000, hot_shard_bias=0.7):
    # 70% of traffic goes to Shard 0 (e.g. VIP tenant)
    shard_load = defaultdict(int)
    for _ in range(total_requests):
        if random.random() < hot_shard_bias:
            shard_load[0] += 1
        else:
            s = random.randint(1, num_shards - 1)
            shard_load[s] += 1
    return shard_load

if __name__ == "__main__":
    random.seed(42)
    loads = simulate_traffic(num_shards=5, total_requests=10000, hot_shard_bias=0.75)
    print("Simulated Request Distribution across 5 Shards:")
    for s in range(5):
        pct = (loads[s] / 10000) * 100
        bar = "#" * int(pct // 2)
        print(f"  Shard [{s}]: {loads[s]:5d} requests ({pct:5.1f}%) | {bar}")
    print("\\nShard 0 is a HOT SHARD absorbing 75% of total cluster work!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 55: Hot Shards & Load Imbalance ==="
python3 phases/55-hot-shards/code/55_hot_shards.py
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
    generate_phases_42_to_55()
