# Lesson 00.1: Environment and Search Lab

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
curl -o /dev/null -s -w 'Total time: %{time_total}s\n' http://localhost:9200/
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
